import playwright

from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     page = browser.new_page()
#     page.goto("https://google.com")
#     page.get_by_role("combobox").fill("playwright python")
#     page.wait_for_timeout(1000)
#     page.keyboard.press("Enter")
#     page.wait_for_timeout(1000)
#     page.screenshot(path="screenshot.png")
    
#     page.locator("input[type='file']").set_input_files("screenshot.png")
#     # 若有多張圖片，就用 set_input_files(["image1.jpg","image2.jpg","image3.jpg",])


#     input()
#     browser.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel="chrome")
    context = browser.new_context(storage_state="shopee_state.json")
    context.set_default_timeout(10000)
    page = context.new_page()
    page.goto("https://seller.shopee.tw/portal/product/new?from=sidebar")

    # 遇到雙 class 時，記得兩個 class 最前面都要加上.，且中間不用空格隔開
    # page.wait_for_selector(".eds-icon.eds-modal__close").click()
    # 可以用 locator，自帶等待效果，適合需要操作元素時使用。
    page.screenshot(path="screenshot1.png")
    page.wait_for_timeout(2000)
    input("按下enter開始上傳圖片")
    image_list = ["screenshot.png","screenshot1.png"]
    page.locator(".shopee-image-manager__content input.eds-upload__input").first.set_input_files(image_list)
    
    if 1==0:
        try:
            # 可用空格隔開上下階級的 class
            page.locator(".text-popup-window-modal i.eds-icon.eds-modal__close").first.click()
        except:
            pass    
    input("登入後按下 enter 繼續")
    context.storage_state(path="shopee_state.json")
    browser.close()

#<div data-v-bbefe8c8="" class="shopee-image-manager__content"><div data-v-bbefe8c8="" class="shopee-image-manager__upload"><div data-v-05d7aace="" data-v-bbefe8c8="" class="shopee-file-upload" accept="image/*"><div data-v-558570d9="" data-v-05d7aace="" class="popover-wrap field-disabled-tips"><div data-v-18852921="" data-v-05d7aace="" class="eds-upload" simple="false" aspect="1"><div data-v-18852921="" class="eds-upload-wrapper eds-upload-dragger"><input data-v-18852921="" simple="false" aspect="1" class="eds-upload__input" type="file" name="file" accept="image/*" multiple=""><div data-v-bbefe8c8="" class="shopee-image-manager__upload__content"><div data-v-bbefe8c8="" class="shopee-image-manager__upload__content__icon"><i data-v-ef5019c0="" data-v-bbefe8c8="" class="eds-icon"><svg viewBox="0 0 23 21" xmlns="http://www.w3.org/2000/svg"><path d="M18.5 0C19.3284 0 20 0.671573 20 1.5V12C19.5101 11.9299 18.9899 11.9299 18.5 12V1.5H2V14.1495L5.39451 10.7424C5.65509 10.4808 6.06062 10.4517 6.35341 10.6552L6.45741 10.7424L7.88894 12.1801L11.5762 6.9708C11.8367 6.70911 12.2423 6.68004 12.5351 6.88357L12.6391 6.9708L16.0301 10.3761C16.8392 11.1887 16.4631 12.6552 15.6322 13.4455C14.6267 14.4019 14 15.7528 14 17.25C14 17.5046 14.0181 17.755 14.0532 18H2C1.17157 18 0.5 17.3284 0.5 16.5V1.5C0.5 0.671573 1.17157 0 2 0H18.5Z"></path><path d="M6.5 4.5C7.32843 4.5 8 5.17157 8 6C8 6.82843 7.32843 7.5 6.5 7.5C5.67157 7.5 5 6.82843 5 6C5 5.17157 5.67157 4.5 6.5 4.5Z"></path><path d="M18.5 14.25C18.5 13.8358 18.8358 13.5 19.25 13.5C19.6642 13.5 20 13.8358 20 14.25V16.5H22.25C22.6642 16.5 23 16.8358 23 17.25C23 17.6642 22.6642 18 22.25 18H20V20.25C20 20.6642 19.6642 21 19.25 21C18.8358 21 18.5 20.6642 18.5 20.25V18H16.25C15.8358 18 15.5 17.6642 15.5 17.25C15.5 16.8358 15.8358 16.5 16.25 16.5H18.5V14.25Z"></path></svg></i></div><div data-v-bbefe8c8="" class="shopee-image-manager__upload__content__text">新增圖片 (0/9) </div></div></div></div></div></div></div></div>
# <div data-v-18852921="" data-v-05d7aace="" class="eds-upload" 
#<div data-v-bbefe8c8="" class="shopee-image-manager__itembox" style="width: 80px; max-width: 80px; height: 80px; max-height: 80px;"><div data-v-bbefe8c8="" class="shopee-image-manager__content"><div data-v-bbefe8c8="" class="shopee-image-manager__upload"><div data-v-05d7aace="" data-v-bbefe8c8="" class="shopee-file-upload" accept="image/*"><div data-v-558570d9="" data-v-05d7aace="" class="popover-wrap field-disabled-tips"><div data-v-18852921="" data-v-05d7aace="" class="eds-upload" simple="false" aspect="1"><div data-v-18852921="" class="eds-upload-wrapper eds-upload-dragger"><input data-v-18852921="" simple="false" aspect="1" class="eds-upload__input" type="file" name="file" accept="image/*" multiple=""><div data-v-bbefe8c8="" class="shopee-image-manager__upload__content"><div data-v-bbefe8c8="" class="shopee-image-manager__upload__content__icon"><i data-v-ef5019c0="" data-v-bbefe8c8="" class="eds-icon"><svg viewBox="0 0 23 21" xmlns="http://www.w3.org/2000/svg"><path d="M18.5 0C19.3284 0 20 0.671573 20 1.5V12C19.5101 11.9299 18.9899 11.9299 18.5 12V1.5H2V14.1495L5.39451 10.7424C5.65509 10.4808 6.06062 10.4517 6.35341 10.6552L6.45741 10.7424L7.88894 12.1801L11.5762 6.9708C11.8367 6.70911 12.2423 6.68004 12.5351 6.88357L12.6391 6.9708L16.0301 10.3761C16.8392 11.1887 16.4631 12.6552 15.6322 13.4455C14.6267 14.4019 14 15.7528 14 17.25C14 17.5046 14.0181 17.755 14.0532 18H2C1.17157 18 0.5 17.3284 0.5 16.5V1.5C0.5 0.671573 1.17157 0 2 0H18.5Z"></path><path d="M6.5 4.5C7.32843 4.5 8 5.17157 8 6C8 6.82843 7.32843 7.5 6.5 7.5C5.67157 7.5 5 6.82843 5 6C5 5.17157 5.67157 4.5 6.5 4.5Z"></path><path d="M18.5 14.25C18.5 13.8358 18.8358 13.5 19.25 13.5C19.6642 13.5 20 13.8358 20 14.25V16.5H22.25C22.6642 16.5 23 16.8358 23 17.25C23 17.6642 22.6642 18 22.25 18H20V20.25C20 20.6642 19.6642 21 19.25 21C18.8358 21 18.5 20.6642 18.5 20.25V18H16.25C15.8358 18 15.5 17.6642 15.5 17.25C15.5 16.8358 15.8358 16.5 16.25 16.5H18.5V14.25Z"></path></svg></i></div><div data-v-bbefe8c8="" class="shopee-image-manager__upload__content__text">新增圖片 (0/9) </div></div></div></div></div></div></div></div></div>


