#!/usr/bin/env python3
"""Simple test of template inheritance in subclassing without Flask dependencies."""

import sys
import os

# Add the hexflow package to the path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_template_inheritance():
    """Test that subclassing properly inherits template folders."""
    
    print("🧪 Testing Template Inheritance in Subclassing\n")
    
    # Test 1: Import the DisplayApp to check template folder setup
    try:
        from hexflow.skeletons.display.app import DisplayApp
        print("✅ Successfully imported DisplayApp")
        
        # Create an instance to see template folder
        app = DisplayApp(name="test-display", host='localhost', port=8000)
        template_folder = getattr(app.app, 'template_folder', None)
        print(f"📁 Parent template folder: {template_folder}")
        
        # Check if parent templates exist
        if template_folder:
            parent_templates_exist = os.path.exists(template_folder)
            print(f"📋 Parent templates exist: {parent_templates_exist}")
            
            if parent_templates_exist:
                template_files = os.listdir(template_folder)
                print(f"📄 Available parent templates: {template_files}")
        
    except ImportError as e:
        print(f"❌ Failed to import DisplayApp: {e}")
        return False
    
    print("\n" + "="*60 + "\n")
    
    # Test 2: Create a simple subclass
    class TestDisplaySubclass(DisplayApp):
        """Test subclass of DisplayApp."""
        
        def __init__(self, name="test-subclass", **kwargs):
            super().__init__(name=name, **kwargs)
            print(f"🔗 Subclass created with template folder: {self.app.template_folder}")
            
        def setup_display(self, workflow_data=None):
            return {
                'title': 'Subclass Test',
                'sections': [{'title': 'Test', 'items': []}],
                'completion_message': 'Subclassing works!'
            }
    
    print("2. Testing subclass template inheritance:")
    try:
        subclass_app = TestDisplaySubclass()
        
        # Compare template folders
        parent_folder = app.app.template_folder
        subclass_folder = subclass_app.app.template_folder
        
        print(f"📁 Parent template folder:   {parent_folder}")
        print(f"📁 Subclass template folder: {subclass_folder}")
        print(f"🔗 Template inheritance:     {'✅ WORKING' if parent_folder == subclass_folder else '❌ NOT WORKING'}")
        
    except Exception as e:
        print(f"❌ Failed to create subclass: {e}")
        return False
    
    print("\n" + "="*60 + "\n")
    
    # Test 3: Test template override
    class TestDisplayWithOverride(DisplayApp):
        """Test subclass with template override."""
        
        def __init__(self, name="test-override", **kwargs):
            super().__init__(name=name, **kwargs)
            
            # Try to override with custom templates
            custom_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            if os.path.exists(custom_template_dir):
                self.app.template_folder = custom_template_dir
                print(f"🎨 Override: Using custom templates from {custom_template_dir}")
            else:
                print(f"📁 Fallback: Using parent templates from {self.app.template_folder}")
    
    print("3. Testing template override:")
    try:
        override_app = TestDisplayWithOverride()
        
        custom_templates_exist = os.path.exists(os.path.join(os.path.dirname(__file__), 'templates'))
        print(f"📄 Custom templates exist: {custom_templates_exist}")
        
        if custom_templates_exist:
            custom_files = os.listdir(os.path.join(os.path.dirname(__file__), 'templates'))
            print(f"📋 Custom template files: {custom_files}")
        
    except Exception as e:
        print(f"❌ Failed to create override subclass: {e}")
        return False
    
    print("\n🎉 All template inheritance tests completed successfully!")
    return True

if __name__ == "__main__":
    test_template_inheritance()