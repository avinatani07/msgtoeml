"""
Test MSG to EML Conversion - Standalone Script
Tests only the conversion logic without Azure Function or Blob Storage
"""

import sys
from pathlib import Path
from services.msg_converter import MSGConverter

def test_conversion(msg_file_path: str):
    """Test MSG to EML conversion with a local file"""
    
    print("🧪 Testing MSG to EML Conversion")
    print("=" * 60)
    
    # Check if file exists
    msg_path = Path(msg_file_path)
    if not msg_path.exists():
        print(f"❌ Error: File not found: {msg_file_path}")
        return
    
    print(f"📄 Input file: {msg_path.name}")
    print(f"📊 File size: {msg_path.stat().st_size:,} bytes")
    print()
    
    # Read the MSG file
    try:
        with open(msg_path, 'rb') as f:
            msg_data = f.read()
        print("✅ File read successfully")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    # Initialize converter
    converter = MSGConverter()
    
    # Test conversion
    print("\n🔄 Converting MSG to EML...")
    print("-" * 60)
    
    try:
        eml_content = converter.convert_msg_to_eml(msg_data, msg_path.name)
        
        print("✅ CONVERSION SUCCESSFUL!")
        print()
        print("📧 EML Content Preview:")
        print("=" * 60)
        
        # Show first 1000 characters of EML
        preview = eml_content[:1000]
        print(preview)
        
        if len(eml_content) > 1000:
            print(f"\n... (showing first 1000 of {len(eml_content)} characters)")
        
        print("=" * 60)
        print()
        
        # Save to file
        output_file = msg_path.stem + ".eml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(eml_content)
        
        print(f"💾 Saved to: {output_file}")
        print(f"📊 Output size: {len(eml_content):,} characters")
        
        # Show some stats
        print()
        print("📊 Conversion Stats:")
        print("-" * 60)
        lines = eml_content.split('\n')
        print(f"Total lines: {len(lines)}")
        
        # Count headers
        header_count = 0
        for line in lines:
            if line and ':' in line and not line.startswith(' '):
                header_count += 1
            elif line == '':
                break
        
        print(f"Email headers: {header_count}")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ CONVERSION FAILED!")
        print(f"Error: {str(e)}")
        print()
        
        # Show more details
        import traceback
        print("📋 Error Details:")
        print("-" * 60)
        traceback.print_exc()
        
        return False

def main():
    """Main function"""
    
    if len(sys.argv) < 2:
        print("Usage: python test_conversion_only.py <path_to_msg_file>")
        print()
        print("Example:")
        print("  python test_conversion_only.py my_email.msg")
        print("  python test_conversion_only.py \"C:\\path\\to\\email.msg\"")
        print()
        print("Note: You need a REAL MSG file from Microsoft Outlook")
        print("      (File → Save As → Outlook Message Format)")
        return
    
    msg_file = sys.argv[1]
    test_conversion(msg_file)

if __name__ == "__main__":
    main()
