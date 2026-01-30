#!/usr/bin/env python3
"""
Consent Seeding Script

This script generates and uploads consent documents for patients in the Identity Service
using the Consent Ingestion API. It creates realistic consent scenarios across different
disease categories.

Usage:
    python seed_consents.py [--dry-run] [--identity-url URL] [--consent-url URL]
"""

import argparse
import requests
import sys
from datetime import datetime, timedelta
from io import BytesIO
from typing import List, Dict
import time

from consent_templates import get_consent_template


# Default service URLs
DEFAULT_IDENTITY_URL = "http://localhost:8010"
DEFAULT_CONSENT_URL = "http://localhost:8002"


class ConsentSeeder:
    def __init__(self, identity_url: str, consent_url: str, dry_run: bool = False):
        self.identity_url = identity_url
        self.consent_url = consent_url
        self.dry_run = dry_run
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def get_patients_by_category(self, abha_prefix: str) -> List[Dict]:
        """Fetch patients from Identity Service by ABHA ID prefix"""
        try:
            all_patients = []
            offset = 0
            limit = 100
            
            while True:
                response = requests.get(
                    f"{self.identity_url}/api/v1/patients",
                    params={"limit": limit, "offset": offset}
                )
                response.raise_for_status()
                
                patients = response.json()
                if not patients:
                    break
                
                # Filter by ABHA prefix
                filtered = [p for p in patients if p.get('abha_id', '').startswith(abha_prefix)]
                all_patients.extend(filtered)
                
                # If we got fewer than limit, we've reached the end
                if len(patients) < limit:
                    break
                    
                offset += limit
            
            return all_patients
        except Exception as e:
            print(f"Error fetching patients: {e}")
            return []
    
    def create_consent_text_file(self, consent_text: str, filename: str) -> BytesIO:
        """Create a text file in memory for upload"""
        file_obj = BytesIO(consent_text.encode('utf-8'))
        file_obj.name = filename
        return file_obj
    
    def upload_consent(self, patient_id: str, consent_text: str, abha_id: str) -> bool:
        """Upload consent document via Consent Ingestion API"""
        if self.dry_run:
            print(f"  [DRY RUN] Would upload consent for patient {patient_id} (ABHA: {abha_id})")
            return True
        
        try:
            # Create text file
            file_obj = self.create_consent_text_file(consent_text, f"consent_{abha_id}.txt")
            
            # Prepare multipart form data
            files = {
                'file': (f'consent_{abha_id}.txt', file_obj, 'text/plain')
            }
            data = {
                'patient_id': patient_id
            }
            
            # Upload to Consent Ingestion
            response = requests.post(
                f"{self.consent_url}/consents/upload",
                files=files,
                data=data
            )
            
            if response.status_code in [200, 201]:
                print(f"  ✓ Uploaded consent for patient {abha_id}")
                return True
            else:
                print(f"  ✗ Failed to upload consent for {abha_id}: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error uploading consent for {abha_id}: {e}")
            return False
    
    def seed_category_consents(self, category_name: str, abha_prefix: str, 
                               consent_distribution: Dict[str, int]):
        """
        Seed consents for a disease category
        
        Args:
            category_name: Name of the disease category
            abha_prefix: ABHA ID prefix for this category
            consent_distribution: Dict mapping consent types to counts
        """
        print(f"\n{'='*60}")
        print(f"Seeding consents for {category_name}")
        print(f"{'='*60}")
        
        # Get patients in this category
        patients = self.get_patients_by_category(abha_prefix)
        
        if not patients:
            print(f"No patients found for category {category_name}")
            return
        
        print(f"Found {len(patients)} patients in {category_name} category")
        
        # Distribute consent types among patients
        patient_idx = 0
        today = datetime.now().strftime("%Y-%m-%d")
        
        for consent_type, count in consent_distribution.items():
            print(f"\nCreating {count} '{consent_type}' consents...")
            
            for i in range(count):
                if patient_idx >= len(patients):
                    print(f"  Ran out of patients, skipping remaining consents")
                    self.stats['skipped'] += (count - i)
                    break
                
                patient = patients[patient_idx]
                patient_id = patient['id']
                abha_id = patient['abha_id']
                
                # Generate consent text based on type
                if consent_type == 'full_research':
                    consent_text = get_consent_template('full_research', date=today, abha_id=abha_id)
                elif consent_type == 'limited_care':
                    consent_text = get_consent_template('limited_care', date=today, abha_id=abha_id)
                elif consent_type == 'disease_specific':
                    consent_text = get_consent_template(
                        'disease_specific', 
                        date=today, 
                        abha_id=abha_id,
                        disease_name=category_name
                    )
                elif consent_type == 'partial':
                    consent_text = get_consent_template('partial', date=today, abha_id=abha_id)
                elif consent_type == 'ambiguous':
                    consent_text = get_consent_template('ambiguous', abha_id=abha_id)
                elif consent_type == 'expired':
                    consent_text = get_consent_template('expired', abha_id=abha_id)
                elif consent_type == 'revoked':
                    consent_text = get_consent_template('revoked', date=today, abha_id=abha_id)
                else:
                    print(f"  Unknown consent type: {consent_type}, skipping")
                    self.stats['skipped'] += 1
                    patient_idx += 1
                    continue
                
                # Upload consent
                self.stats['total'] += 1
                if self.upload_consent(patient_id, consent_text, abha_id):
                    self.stats['success'] += 1
                else:
                    self.stats['failed'] += 1
                
                patient_idx += 1
                
                # Small delay to avoid overwhelming the API
                if not self.dry_run:
                    time.sleep(0.5)
    
    def seed_all_consents(self):
        """Seed consents for all disease categories"""
        print("\n" + "="*60)
        print("CONSENT SEEDING SCRIPT")
        print("="*60)
        print(f"Identity Service: {self.identity_url}")
        print(f"Consent Ingestion: {self.consent_url}")
        print(f"Dry Run: {self.dry_run}")
        print("="*60)
        
        # Define consent distribution for each category
        # Each category has 125 patients - distribute varied consent types
        
        # Diabetes - 125 consents
        self.seed_category_consents(
            "Diabetes",
            "91-2345",
            {
                'full_research': 60,
                'disease_specific': 35,
                'limited_care': 20,
                'partial': 5,
                'ambiguous': 3,
                'expired': 2
            }
        )
        
        # Hypertension - 125 consents
        self.seed_category_consents(
            "Hypertension",
            "91-3456",
            {
                'full_research': 55,
                'disease_specific': 40,
                'partial': 15,
                'limited_care': 10,
                'ambiguous': 3,
                'revoked': 2
            }
        )
        
        # Cardiovascular - 125 consents
        self.seed_category_consents(
            "Cardiovascular Disease",
            "91-4567",
            {
                'full_research': 65,
                'disease_specific': 35,
                'limited_care': 15,
                'partial': 5,
                'expired': 3,
                'ambiguous': 2
            }
        )
        
        # Respiratory - 125 consents
        self.seed_category_consents(
            "Respiratory Disease",
            "91-5678",
            {
                'full_research': 60,
                'disease_specific': 38,
                'partial': 12,
                'limited_care': 10,
                'ambiguous': 3,
                'revoked': 2
            }
        )
        
        # Cancer - 125 consents
        self.seed_category_consents(
            "Cancer",
            "91-6789",
            {
                'full_research': 70,
                'disease_specific': 30,
                'limited_care': 15,
                'partial': 5,
                'revoked': 3,
                'expired': 2
            }
        )
        
        # Print summary
        print("\n" + "="*60)
        print("SEEDING SUMMARY")
        print("="*60)
        print(f"Total consents processed: {self.stats['total']}")
        print(f"Successfully uploaded: {self.stats['success']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print("="*60)
        
        if self.stats['failed'] > 0:
            print("\n⚠ Some consents failed to upload. Check the logs above for details.")
            return False
        else:
            print("\n✓ All consents seeded successfully!")
            return True


def main():
    parser = argparse.ArgumentParser(description='Seed consent documents for patients')
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without actually uploading consents'
    )
    parser.add_argument(
        '--identity-url',
        default=DEFAULT_IDENTITY_URL,
        help=f'Identity Service URL (default: {DEFAULT_IDENTITY_URL})'
    )
    parser.add_argument(
        '--consent-url',
        default=DEFAULT_CONSENT_URL,
        help=f'Consent Ingestion URL (default: {DEFAULT_CONSENT_URL})'
    )
    
    args = parser.parse_args()
    
    seeder = ConsentSeeder(
        identity_url=args.identity_url,
        consent_url=args.consent_url,
        dry_run=args.dry_run
    )
    
    success = seeder.seed_all_consents()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
