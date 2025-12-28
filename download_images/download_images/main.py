from selenium import webdriver
from PIL import Image
import io

html_content = "<html><body><h1>Hello, World!</h1></body></html>"

driver = webdriver.Chrome()
driver.get("data:text/html;charset=utf-8," + html_content)
screenshot = driver.get_screenshot_as_png()
driver.quit()

image = Image.open(io.BytesIO(screenshot))
image.save("output.png")