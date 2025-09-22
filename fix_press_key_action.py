#!/usr/bin/env python3
"""
Fix for PressKeyAction not being recognized in strands_tools.browser
"""

def fix_press_key_action():
    """Add PressKeyAction to the browser models if missing"""
    try:
        from strands_tools.browser.models import PressKeyAction
        print("✅ PressKeyAction already available")
        return True
    except ImportError:
        print("❌ PressKeyAction not found, attempting to add it...")
        
        try:
            # Try to patch the models module
            import strands_tools.browser.models as models
            from dataclasses import dataclass
            from typing import Optional
            
            @dataclass
            class PressKeyAction:
                """Action to press a key"""
                key: str
                modifiers: Optional[list] = None
                
            # Add to models module
            models.PressKeyAction = PressKeyAction
            print("✅ PressKeyAction patched successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to patch PressKeyAction: {e}")
            return False

if __name__ == "__main__":
    fix_press_key_action()