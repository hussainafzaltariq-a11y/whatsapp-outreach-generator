import pandas as pd
from typing import List, Dict

class CSVHandler:
    @staticmethod
    def read_leads(file_path: str) -> List[Dict]:
        """Read leads from CSV file"""
        try:
            df = pd.read_csv(file_path)
            required_columns = ['business_name', 'business_type', 'pain_point', 'contact_name']
            
            # Validate columns
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f"Error reading CSV: {str(e)}")
    
    @staticmethod
    def validate_csv_structure(file) -> bool:
        """Validate CSV file structure"""
        try:
            df = pd.read_csv(file)
            required_columns = ['business_name', 'business_type', 'pain_point', 'contact_name']
            return all(col in df.columns for col in required_columns)
        except:
            return False
    
    @staticmethod
    def export_messages(messages: List[Dict], output_path: str):
        """Export generated messages to CSV"""
        df = pd.DataFrame(messages)
        df.to_csv(output_path, index=False)
        return output_path