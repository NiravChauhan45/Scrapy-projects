from selenium import webdriver

# Launch browser
driver = webdriver.Chrome()

# Open your page
driver.get("https://www.bigbasket.com/")

# Inject CSS to hide the cursor inside the page
driver.execute_script("""
    var style = document.createElement('style');
    style.innerHTML = '* { cursor: none !important; }';
    document.head.appendChild(style);
""")
