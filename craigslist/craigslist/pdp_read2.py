import datetime
import hashlib
import json
import os.path
import re
import html
from parsel import Selector
import pymysql
from select import select


def insert_data(table, item):
    field_list = []
    value_list = []
    for field in item:
        field_list.append(str(field))
        value_list.append('%s')
    fields = ",".join(field_list)
    fields = fields.replace('condition', '`condition`')
    values = ", ".join(value_list)
    insert_db = f"insert ignore into {table}( " + fields + " ) values ( " + values + " )"
    try:
        cur.execute(insert_db, tuple(item.values()))
        con.commit()
        print('Inserted')
    except Exception as e:
        print(insert_db, tuple(item.values()))

        if 'duplicate' not in str(e).lower():
            print(e)
        else:
            print(e)
# print()
def create_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8', errors='ignore'))
    return md5_hash.hexdigest()
def pdp_read():
    deleted = []

    # cur.execute("select * from pdp_links_30052025 ")
    cur.execute("SELECT pdp_url FROM `pdp_links_30052025` WHERE pdp_url NOT IN (SELECT product_url FROM `pdp_data_30052025`)")
    rows = cur.fetchall()
    for row in rows:
    #     name = row['name']
    #     price = row['price']
        pdp_url = row['pdp_url']
        # location = row['location']
        # category = row['category']
        # city = row['city']
        hashid = create_md5_hash(pdp_url)
        pagesave_path = fr'D:\Smitesh\pagesave\craigslist\pdp\{hashid}.html'
        # pagesave_path = fr'C:\Users\Actowiz\Desktop\pagesave\craigslist\pdp\{hashid}.html'
        if os.path.exists(pagesave_path):
                f = open(pagesave_path, 'r', encoding='utf8')
                data = f.read()
                if 'This posting has been deleted by its author' not in data:
                    selector = Selector(data)

                    des = selector.xpath('//section[@id="postingbody"]/text()').getall()
                    description = ' '.join(des).strip()

                    product_id = re.findall('post id: (.*?)<', data)[0]
                    posted_date = re.findall('posted: <time class="date timeago" datetime="(.*?)"', data)[0][:-8].replace('T', ' ')
                    try:updated_date = re.findall('updated: <time class="date timeago" datetime="(.*?)"', data)[0][:-8].replace('T', ' ')
                    except:updated_date = ''
                    condition = selector.xpath("//div[contains(@class,'condition')]//a/text()").get('')

                    jsn1_raw = selector.xpath("//script[@id='ld_posting_data']/text()").get()
                    if jsn1_raw:
                        jsn1_raw = jsn1_raw.strip()
                        jsn1 = json.loads(jsn1_raw)
                        # description = jsn1['description'].strip()
                        if description:
                            description = html.unescape(description)
                        name = jsn1['name'].strip()
                        currency = jsn1['offers']['priceCurrency']
                        price = jsn1['offers']['price']
                        lat = jsn1['offers']['availableAtOrFrom']['geo']['latitude']
                        lng = jsn1['offers']['availableAtOrFrom']['geo']['longitude']
                        address_locality = jsn1['offers']['availableAtOrFrom']['address']['addressLocality']
                        postalcode = jsn1['offers']['availableAtOrFrom']['address']['postalCode']
                        address_country = jsn1['offers']['availableAtOrFrom']['address']['addressCountry']
                        address_region = jsn1['offers']['availableAtOrFrom']['address']['addressRegion']
                        street_address = jsn1['offers']['availableAtOrFrom']['address']['streetAddress']
                        images_list = jsn1['image']
                        images_list = [i.replace('600x450', '1200x900') for i in images_list]
                        image = '|'.join(images_list)
                        current_time = datetime.datetime.now(datetime.timezone.utc)
                        timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                        add_list = [i for i in [street_address, address_locality, postalcode, address_country, address_region] if i != '']
                        attributes_label = selector.xpath("//div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='labl']/text()").getall()
                        # attributes_value = selector.xpath("//div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='valu']/text()").getall()
                        attributes_value = selector.xpath("//div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='valu']/text() | //div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='valu']/a/text()").getall()
                        attributes_value = [i.strip() for i in attributes_value if i.strip() != '']
                        attributes = {}
                        # if condition:
                        #     attributes['condition'] = condition
                        for labl, valu in zip(attributes_label, attributes_value):
                            labl = labl.replace(':', '')
                            attributes[labl] = valu





                        cat = selector.xpath('//li[@class="crumb category"]//a/text()').get()
                        item = {}
                        item['listing_id'] = product_id
                        # item['source'] = 'craigslist'
                        item['scrape_timestamp'] = str(timestamp)
                        item['description'] = description
                        item['category'] = cat
                        item['address'] = ', '.join(add_list)
                        item['created_date'] = posted_date
                        item['updated_date'] = updated_date
                        item['attributes'] = json.dumps(attributes)
                        # item['sold_date'] = ''
                        # item['gtin'] = ''
                        # item['mpn'] = ''
                        item['price'] = price
                        item['currency'] = currency
                        item['condition'] = condition
                        item['images'] = image
                        item['product_id'] = product_id
                        item['product_url'] = pdp_url
                        item['product_title'] = name
                        item['listing_url'] = 'https://newyork.craigslist.org/search/sss?excats=20-22-2-25-4-46-3-2-21-1-14-1-2-1-4-22-1-1-1-1-11-1&isTrusted=true#search=2~gallery~0'
                        # item['quantity'] = ''

                        insert_data('pdp_data_30052025', item)
                        # cur.execute(f"update pdp_links set status='done' where pdp_url='{pdp_url}'")
                        # con.commit()
                        print(pdp_url)
                    else:
                        name = selector.xpath("//*[@class='postingtitle']//*[@id='titletextonly']/text()").get()
                        price = selector.xpath("//*[@class='postingtitle']//*[@*='price']/text()").get('')
                        currency = re.sub(r'[\d.,]', '', price)
                        images_tag = selector.xpath("//div[@class='gallery']//*[@*='swipe-wrap']//@data-imgid").getall()
                        images_list = [f'https://images.craigslist.org/00A0A_{img_tag}_1200x900.jpg' for img_tag in images_tag]
                        image = '|'.join(images_list)
                        address = selector.xpath("//*[@class='postingtitle']//*[not(@*)]/text()").get()
                        if address:
                            address = address.replace('(', '').replace(')', '').strip()
                        current_time = datetime.datetime.now(datetime.timezone.utc)
                        timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                        attributes_label = selector.xpath(
                            "//div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='labl']/text()").getall()
                        # attributes_value = selector.xpath("//div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='valu']/text()").getall()
                        attributes_value = selector.xpath(
                            "//div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='valu']/text() | //div[@class='attrgroup']//div[not(contains(@class,'condition'))]//*[@class='valu']/a/text()").getall()
                        attributes_value = [i.strip() for i in attributes_value if i.strip() != '']
                        attributes = {}
                        # if condition:
                        #     attributes['condition'] = condition
                        for labl, valu in zip(attributes_label, attributes_value):
                            labl = labl.replace(':', '')
                            attributes[labl] = valu

                        cat = selector.xpath('//li[@class="crumb category"]//a/text()').get()
                        item = {}
                        item['listing_id'] = product_id
                        # item['source'] = 'craigslist'
                        item['scrape_timestamp'] = str(timestamp)
                        item['description'] = description
                        item['category'] = cat
                        item['address'] = address
                        item['created_date'] = posted_date
                        item['updated_date'] = updated_date
                        item['attributes'] = json.dumps(attributes)
                        # item['sold_date'] = ''
                        # item['gtin'] = ''
                        # item['mpn'] = ''
                        item['price'] = price
                        item['currency'] = currency
                        item['condition'] = condition
                        item['images'] = image
                        item['product_id'] = product_id
                        item['product_url'] = pdp_url
                        item['product_title'] = name
                        item[
                            'listing_url'] = 'https://newyork.craigslist.org/search/sss?excats=20-22-2-25-4-46-3-2-21-1-14-1-2-1-4-22-1-1-1-1-11-1&isTrusted=true#search=2~gallery~0'
                        # item['quantity'] = ''

                        insert_data('pdp_data_30052025', item)
                        # cur.execute(f"update pdp_links set status='done' where pdp_url='{pdp_url}'")
                        # con.commit()
                        print(pdp_url)


                else:deleted.append(hashid)
    print(deleted)





if __name__ == '__main__':
    # con = pymysql.connect(host='localhost', user='root', password='actowiz', database='craigslist')
    # cur = con.cursor(pymysql.cursors.DictCursor)
    # rows = [
    #     "https://newyork.craigslist.org/fct/ele/d/greenwich-sharp-hdtv-lcd-flat-screen/7820616610.html",
    #     "https://newyork.craigslist.org/fct/ele/d/greenwich-insignia-hdtv/7818851493.html",
    #     "https://newyork.craigslist.org/wch/ele/d/larchmont-iphone-ipad-htc-extras/7832822123.html",
    #     "https://newyork.craigslist.org/wch/ele/d/mamaroneck-nikon-digital-camera/7829910718.html",
    #     "https://newyork.craigslist.org/wch/ele/d/larchmont-klh-speakers/7829909912.html",
    #     "https://newyork.craigslist.org/wch/ele/d/larchmont-victoria-classic-retro-with/7831673294.html",
    #     "https://newyork.craigslist.org/wch/ele/d/larchmont-jamo-subwoofers-a3-sub5/7829910354.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-sony-dvp-ns575p-progressive-scan/7838381606.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/westbury-kenwood-car-audio-amp-kenwood/7821428739.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/westbury-peavey-km-keyboard-mixer/7817373442.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/westbury-riders-volumes-vi-to-xiii/7821429101.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/westbury-diehl-vintage-military/7822525121.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/westbury-vintage-jvc-boom-box-pc-sounds/7821428284.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/amityville-camera-canon-eos-rebel-2000/7822514669.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/great-neck-jbl-bluetooth-speaker-charge/7839464000.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/sharp-flat-screen-tv/7817818655.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/amityville-camera-canon-eos-rebel-body/7822514702.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/amityville-camera-expodisc/7822514693.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/amityville-camera-filters/7822514749.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/amityville-camera-olympus-infinity-zoom/7822514697.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-micro-switches-bz-2rq9/7844505935.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-hifiman-he1000-v2-planar/7829057708.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-vtech-wideband-office-headsets/7829058078.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/linksys-ac1300-media-converter-wumc710/7829062146.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-jaybird-bluebuds-sport-sweat/7829060927.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-city-samsung-galaxy-gear-s2/7829061894.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-city-trendnet-tha-103ac-home/7829059790.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-zoopa-q250-prime-raider-drone/7829061002.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-sennheiser-rs195-digital-tv/7829057168.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/pebble-smartwatch-pink-band-for-samsung/7829059631.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-bambu-lab-ams-lite-new-open-box/7844504891.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-apple-tv-4k-64-gb/7843059400.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-110v-wall-outlet-slot-lithium/7843493544.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-new-12v-electric-car-compact/7842357553.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-insignia-32-screen-lcd-tv-flat/7843523894.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-nintendo-swith2/7844503540.html",
    #     "https://newyork.craigslist.org/que/ele/d/kew-gardens-bose-headset-not-perfect/7830207971.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-casio-shock-gm-5600ub/7843831449.html",
    #     "https://newyork.craigslist.org/que/ele/d/kew-gardens-apple-ipod-32gb-extras/7840481334.html",
    #     "https://newyork.craigslist.org/fct/ele/d/ridgefield-sony-dual-tape-deck-tc-w300/7830797817.html",
    #     "https://newyork.craigslist.org/brx/ele/d/new-rochelle-yuasa-battery/7844502279.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-papago-2k-dual-dashboard/7830880362.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-samsung-55-inch-class-qled-4k/7818342510.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-pack-led-light-bulbs-g25-globe/7817108807.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-samsung-43-inch-class-qled-4k/7817506200.html",
    #     "https://newyork.craigslist.org/wch/ele/d/new-rochelle-calculator-in-new-condition/7844501640.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/baldwin-portable-bluetooth-speaker-ion/7827372028.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-panduit-cj688tgbu-mini-com/7829064089.html",
    #     "https://newyork.craigslist.org/stn/ele/d/staten-island-les-paul-gibson-guitar/7844500664.html",
    #     "https://newyork.craigslist.org/jsy/ele/d/flanders-xerox-workcentre-6400-color/7830250906.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-vacuum-tubes/7838909480.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/baldwin-canon-pixma-printer-ip4760/7819081202.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-belkin-surge-protectors/7833453470.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zippo-hand-warmer-power-bank/7831534106.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-rode-shotgun-mic/7822457846.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-dygma-raise-ergonomic-split/7833838462.html",
    #     "https://newyork.craigslist.org/wch/ele/d/mount-vernon-miele-quick-step-upright/7830789088.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-samsung-tv-mini-wall-mount/7824037914.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-wall-mount-for-sonos-one-one/7824037457.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-conrad-johnson-18ls-stereo/7833008412.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-apple-watch-trail-loop-watch-band/7823381899.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-asus-32-4k-pg32uq-hdmi-21-gaming/7823381526.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-adcom-gfa-power-amplifier/7833005513.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-mx-keys-keyboard-for-pc/7823381193.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-anker-in-cube-with-magsafe/7823381016.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-gymax-inflatable-bounce-house/7823380657.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sennheiser-ch800s-balanced/7820139841.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-mx-keys-for-mac-logitech-keyboard/7823380205.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-apple-watch-band-alpine-loop-49mm/7823379860.html",
    #     "https://newyork.craigslist.org/brx/ele/d/bronx-15-pro-max-natural-titanium-256gb/7830727030.html",
    #     "https://newyork.craigslist.org/que/ele/d/forest-hills-original-nintendo-wii-for/7835668165.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-birdog-satellite-meter/7833575694.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-emerson-30-flat-lcd-screen-tv/7833578377.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-apple-magsafe-charger/7836534773.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-canon-pixma-mx340-wireless/7833575547.html",
    #     "https://newyork.craigslist.org/que/ele/d/rego-park-frontera-750-ml-received-gift/7837551241.html",
    #     "https://newyork.craigslist.org/que/ele/d/rego-park-fest-750-ml/7837551359.html",
    #     "https://newyork.craigslist.org/que/ele/d/rego-park-iphone-10-foot-usb-to/7818706936.html",
    #     "https://newyork.craigslist.org/que/ele/d/rego-park-kenwood-pro-talk-walkie/7832806374.html",
    #     "https://newyork.craigslist.org/que/ele/d/rego-park-fest-750-ml/7837551457.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-skyway-fingertip-pulse-oximeter/7829566641.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-g40-replacement-light-bulbs/7827328160.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-electric-amazon-items/7843823161.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-hp-envy-photo-7855-inkjet/7844487202.html",
    #     "https://newyork.craigslist.org/que/ele/d/forest-hills-lg-32-flat-screen-tv-lh30/7841629538.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-weller-wxd2-desoldering/7825144117.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-brand-new-sealed-apple-watch/7831427541.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-brand-new-apple-magic-keyboard/7841070017.html",
    #     "https://newyork.craigslist.org/que/ele/d/jamaica-microsoft-surface-pro-i5-6300u/7821408799.html",
    #     "https://newyork.craigslist.org/que/ele/d/jamaica-viewsonic-vx2485-mhu-ips-monitor/7821408779.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-apple-airpods-pro-2nd/7844481956.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-ring-video-doorbell-pro/7843280350.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-google-chromecast-3rd/7842506881.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-google-chromecast-audio/7842507030.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-google-nest-thermostat/7842507269.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-wyze-smart-doorbell-sense/7842507432.html",
    #     "https://newyork.craigslist.org/lgi/ele/d/middle-village-heygelo-drone-s90-for/7824733867.html",
    #     "https://newyork.craigslist.org/que/ele/d/lg-tablet-for-sale-lg-lk430/7819018315.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-all-type-of-linen/7844481446.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-bar-adjustable-high/7844481126.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/kew-gardens-viltrox-af-56mm-14-lens-for/7833656695.html",
    #     "https://newyork.craigslist.org/que/ele/d/kew-gardens-lg-ultrawide-hz-hdr-ips/7843941337.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-porsche-wheels-and/7844480937.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-hp-laserjet-pro-200/7844480601.html",
    #     "https://newyork.craigslist.org/brk/ele/d/staten-island-lg-led-tv/7843934939.html",
    #     "https://newyork.craigslist.org/stn/ele/d/staten-island-lg-led-tv/7843934896.html",
    #     "https://newyork.craigslist.org/brk/ele/d/staten-island-samsung-40-smart-led-tv/7843941851.html",
    #     "https://newyork.craigslist.org/fct/ele/d/trumbull-asus-215-vp228-lcd-monitor-new/7840246765.html",
    #     "https://newyork.craigslist.org/fct/ele/d/trumbull-denon-multi-zone-receiver/7840244032.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-dilvpoetry-tube-t6-headphone/7833850398.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-smart-humidifier-large-room/7830125251.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-apple-watch-series-brand-new/7824547267.html",
    #     "https://newyork.craigslist.org/brk/ele/d/hp-all-in-one-pc-touch-screen-desktop/7828440157.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-tv-stand-tempered/7844480041.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-set-of-film-holders-for/7836752874.html",
    #     "https://newyork.craigslist.org/que/ele/d/astoria-brand-new-marshall-stanmore-ii/7820411850.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-hp-19b-ii-19bii-hp-business/7825017426.html",
    #     "https://newyork.craigslist.org/que/ele/d/astoria-brand-new-marshall-woburn-iii/7822626438.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-golf-club-bag/7844479139.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-tv-stand-vintage-look/7844478854.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-paintings-portrairs/7844478522.html",
    #     "https://newyork.craigslist.org/stn/ele/d/staten-island-jbl-pulse/7840317497.html",
    #     "https://newyork.craigslist.org/stn/ele/d/staten-island-1970s-cabin-cruiser-boat/7839742717.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-feet-gray-35mm-audio-cable/7823555056.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-glass-screen-protector/7823554958.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-cujo-ai-smart-home-internet/7823554994.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-ultraglass-top-9h-glass-for/7818152460.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-sennheiser-usb-headset/7819531801.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-tvsamsung-43/7844477173.html",
    #     "https://newyork.craigslist.org/que/ele/d/corona-sharp-939z-bombox/7824101719.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-tv-samsung-un40eh5000f/7844476619.html",
    #     "https://newyork.craigslist.org/que/ele/d/corona-sharp-939z-bombox/7826284339.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-blink-mini-compact-indoor-plug/7820787347.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-monoprice-harmony-note/7823264977.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-samsung-hw-q600b-312ch/7836014709.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-jbl-tune-500bt-wireless/7832997711.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-fire-hd-tablet-th-gen-designed/7841825601.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-lowell-lvc8pid2-rack-volume/7820859717.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-romoss-40000mah-portable/7826890003.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-sanus-rack-shelves-heavy-duty/7823218221.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-tronsmart-bang-60w-bluetooth/7827624548.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-tv-panasonic-tc-l32c3/7844476110.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-lenovo-thinkplus-livepods-lp75/7824963343.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-beats-solo3-wireless-on-ear/7824770348.html",
    #     "https://newyork.craigslist.org/brk/ele/d/new-york-gaming-setup/7840362984.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-tv-vizio-39/7844475745.html",
    #     "https://newyork.craigslist.org/que/ele/d/middle-village-fitbit-charge-excellent/7824740007.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-tv-32-sony-model-kdl/7844475219.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-pyramid-4400g-made-in-usa/7827834013.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sansui-x500-receiver/7827833882.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-pyramid-4400g-made-in-usa/7819261388.html",
    #     "https://newyork.craigslist.org/que/ele/d/forest-hills-google-pixel-buds-series/7843339180.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-soundcore-anker-liberty-pro/7833704373.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-vtin-14w-loud-sound-portable/7822458137.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-amazon-fire-tv-stick-4k-max/7836047003.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-taotronics-tt-dl092-12w-led/7819984027.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-amazon-basics-15-feet/7833634310.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-jbl-tune-120tws-true-wireless/7823147973.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-huanuo-single-monitor-mount/7831573124.html",
    #     "https://newyork.craigslist.org/que/ele/d/long-island-city-amazon-fire-tv/7844474617.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-beats-solo3-wireless-on-ear/7827624626.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-phonicgrid-se7-hybrid-active/7818226633.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s39-60w-wireless/7825095339.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-msrp-349-sony-srs-xg300-bz/7833701776.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-soundcore-by-anker-30w-motion/7822200325.html",
    #     "https://newyork.craigslist.org/que/ele/d/flushing-idesign-brookstone-tower/7832467382.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-oraolo-m91-40w-portable/7844472819.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s51-pro-40w-max-outdoor/7837807813.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-prscfum-20w-portable-bluetooth/7819306500.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-edifier-w200t-mini-true/7820459921.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-beats-studio3-wireless-noise/7826227377.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-pheanoo-d5-80w-21ch-wireless/7837644753.html",
    #     "https://newyork.craigslist.org/que/ele/d/flushing-sony-bravia-tv-4o-inch-lcd-tv/7832467663.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-meco-2k-2560-1440-qhd-webcam/7821615158.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-votomy-vt-pick-wireless/7824342885.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-klipsch-t5-ii-active-noise/7820665871.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sennheiser-momentum-true/7835671028.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-altec-lansing-nanobuds-true/7820553937.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-mee-partyspkr-xl-60w-rms-120w/7833342476.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-amovee-acrylic-headphone-stand/7822209405.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-blink-mini-compact-indoor-plug/7820495799.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-lenrue-usb-bluetooth-computer/7833019875.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-victsing-mm057-24g-wireless/7822553849.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-onn-portable-bluetooth-speaker/7822129330.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-ge-cync-smart-led-light-bulbs/7823520364.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-soundcore-by-anker-life-note/7820515530.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-edifier-tws330-nb-true/7820787426.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-soulion-r50-bluetooth-computer/7824105023.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-wrz-n5-wireless-bluetooth/7827150467.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-wenkey-e2-true-wireless/7831144690.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sc208-portable-bluetooth/7822205700.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-ubeesize-67-all-in-one/7821580756.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-pack-griffin-10w-wireless/7835645963.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s56-40w-portable/7835648101.html",
    #     "https://newyork.craigslist.org/que/ele/d/massapequa-park-sony-home-theater/7840202973.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s32pro-15w-portable/7841778969.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-beats-solo3-wireless-on-ear/7835619809.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-erkei-sehn-25w-max-portable/7837312194.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sony-linkbuds-truly-wireless/7837283146.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sennheiser-momentum-true/7823800552.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-monster-aria-free-open-ear-air/7839451540.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-wimuue-40w-wireless-bluetooth/7830068463.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-b21-noise-cancelling/7829496842.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sennheiser-momentum-true/7839198887.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-punkwolf-portable-bluetooth/7819069780.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-aukey-ep-b52-wireless/7821136821.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-msrp-400-akg-n9-hybrid/7832167885.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sony-mdr-e9lp-wired-stereo/7827606091.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-philips-h5209-over-ear/7844472708.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-mee-partyspkr-60w-rms-120w/7833100296.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-blink-mini-compact-indoor-plug/7818912129.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-msrp-office-star-ascend-ii/7820287660.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-topvision-50w-wireless/7839382264.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s51-20w-portable/7823549137.html",
    #     "https://newyork.craigslist.org/que/ele/d/astoria-excellent-dyson-v10-cyclone/7823412398.html",
    #     "https://newyork.craigslist.org/que/ele/d/astoria-brand-new-marshall-acton-ii/7832392206.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-philips-s7505-wireless/7839378527.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-poweradd-musicfly-a1-36w/7844472760.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-msrp-349-sony-wh-1000xm4/7844472517.html",
    #     "https://newyork.craigslist.org/wch/ele/d/yonkers-used-behringer-xenyx-1002sfx-10/7830246024.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-anker-20000mah-15w-power-bank/7844472239.html",
    #     "https://newyork.craigslist.org/wch/ele/d/yonkers-used-onkyo-tx-rz-channel/7830249444.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-topvision-50w-wireless/7844470619.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-samsung-s2-verizon-4g-tablet/7830562472.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-sennheiser-hd-599-se-around/7844470731.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s51-pro-40w-max-outdoor/7844470571.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-amazon-echo-dot-4th-gen-smart/7844470526.html",
    #     "https://newyork.craigslist.org/que/ele/d/elmhurst-crosley-voyager-record-crate/7844470347.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-tcl-55-inch-roku-tv/7844470049.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-rythflo-20w-bluetooth-speaker/7844470036.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-bestergo-aluminum-laptop/7844469633.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-steelies-car-mount-kit-new/7844467918.html",
    #     "https://newyork.craigslist.org/stn/ele/d/staten-island-panasonic-tv-42-high/7844467912.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-riva-iphone-xs-xr-xs-max-case/7833346085.html",
    #     "https://newyork.craigslist.org/mnh/ele/d/new-york-apple-airpods-pro-gen-brand/7828885835.html",
    #     "https://newyork.craigslist.org/que/ele/d/saint-albans-realwear-hands-free/7822798009.html",
    #     "https://newyork.craigslist.org/que/ele/d/saint-albans-kenwood-concert-series-way/7829932621.html",
    #     "https://newyork.craigslist.org/que/ele/d/saint-albans-kenwood-digital-multimedia/7826887835.html",
    #     "https://newyork.craigslist.org/que/ele/d/saint-albans-planet-audio-pcpa975w-din/7819653503.html",
    #     "https://newyork.craigslist.org/que/ele/d/saint-albans-jvc-68-digital-media/7817894243.html",
    #     "https://newyork.craigslist.org/que/ele/d/saint-albans-jvc-68-in-dash-digital/7818572407.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-bugani-m130-portable-10w/7844466229.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-jabra-perform-45-ear-hook-mono/7844466131.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-raymate-s7-bluetooth-speaker/7844464573.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-yw-yuwiss-t04-bluetooth-50/7837810818.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-soundcore-by-anker-space-a40/7839332604.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-soundcore-by-anker-life-dot-nc/7839204346.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-anker-soundcore-flare/7839379169.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s55-20w-outdoor/7827960401.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-altec-lansing-shockwave/7826922247.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-aliergo-a91-soundon-tws-stereo/7819510512.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-monster-mission-200-wireless/7820407614.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-jiga-30000mah-solar-power-bank/7821454217.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-amazon-echo-dot-3rd-gen-voice/7820665422.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-zealot-s32pro-15w-portable/7823744928.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-ubeesize-67-all-in-one/7827177083.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-philips-s7505-wireless/7835733551.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-soundcore-by-anker-life-a1/7824105345.html",
    #     "https://newyork.craigslist.org/brk/ele/d/brooklyn-jbl-vibe-buds-true-wireless/7825370922.html"]
    con = pymysql.connect(host='172.27.131.195', user='root', password='actowiz', database='craigslist')
    cur = con.cursor(pymysql.cursors.DictCursor)
    # cur.execute("select * from pdp_links_30052025 where status='pending'")
    # rows = cur.fetchall()
    # for row in rows:
    #     # row = 'https://newyork.craigslist.org/search/sss?excats=20-22-2-25-4-46-3-2-21-1-14-1-2-1-4-22-1-1-1-1-11-1&isTrusted=true#search=2~gallery~0'

    pdp_read()