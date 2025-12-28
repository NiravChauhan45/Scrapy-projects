from curl_cffi import requests
import re
import logging

from parsel import Selector

from ext.ext_myntra import get_data_pl, get_data_pdp
from rss.config_proxy import *
from rss.retry_handler import with_backoff


logger = logging.getLogger(__name__)

PROXY = None
PROXY_URL = None
if PROXY_MYNTRA:
    if PROXY_MYNTRA_NAME == 'scrapedo':
        PROXY = get_scraper_do_proxy()
        PROXY_URL = get_scraper_do_url()
    elif PROXY_MYNTRA_NAME == 'decodo':
        PROXY = get_decodo_proxy()


def extract_pid(url):
    match = re.search(r'/(\d+)/buy', url)
    if match:
        return match.group(1)
    return None


@with_backoff
def get_pl_response(keyword):
    try:
        url = f'https://www.myntra.com/{keyword}'
        if PROXY_MYNTRA:
            response = requests.get(url=url, proxies=PROXY, verify=False)
        else:
            response = requests.get(url=url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Request failed for keyword {keyword}: {str(e)}")
        raise


@with_backoff
def get_pdp_response(url):
    try:
        if PROXY_MYNTRA:
            pid = re.findall('(\d+)', url)
            url = f'https://www.myntra.com/{pid[0]}'
            response = requests.get(url=url, headers=headers, proxies=PROXY, verify=False)

            selector = Selector(response.text)
            # Extracting the product data embedded in a script tag
            data = selector.xpath(
                "//script[contains(text(), 'window.__myx') and contains(text(), 'pdpData') and contains(text(), 'discountedPrice')]/text()"
            ).get()

            retry = 1
            if not data:
                while True:
                    response = requests.get(url=url, headers=headers, proxies=PROXY, verify=False)

                    selector = Selector(response.text)
                    # Extracting the product data embedded in a script tag
                    data = selector.xpath(
                        "//script[contains(text(), 'window.__myx') and contains(text(), 'pdpData') and contains(text(), 'discountedPrice')]/text()"
                    ).get()
                    if not data:
                        retry += 1
                        if retry == 2:
                            break
                        continue
                    break

            # final_url = get_scraper_do_url() + f"&url={url}"
            # print(final_url)
            # response = requests.get(url=final_url, headers=headers, proxies=PROXY, verify=False)
        else:
            response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Request failed for URL {url}: {str(e)}")
        raise


@with_backoff
def get_similar_response(url):
    proxy_url = get_scraper_do_url()
    pid = extract_pid(url)
    try:
        if PROXY_MYNTRA:
            url = f"{PROXY_URL}&url=https://www.myntra.com/gateway/v2/product/{pid}/related&setCookies=_pv%3Ddefault%3B%20dp%3Dd%3B%20at%3DZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTlROaE5qY3lPR1F0TlRVNU9DMHhNV1l3TFdFM01UQXROR1UzTnpFeE5ESXdNV1EwSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZNE1qa3pNVGNzSW1semN5STZJa2xFUlVFaWZRLkszNGNwT3hQU3hpQ2N5Rzd0dm9KVXB4OGdXRWhoVVJzQ001QVBueHVFWDg%3D%3B%20utm_track_v1%3D%257B%2522utm_source%2522%253A%2522direct%2522%252C%2522utm_medium%2522%253A%2522direct%2522%252C%2522trackstart%2522%253A1751277317%252C%2522trackend%2522%253A1751277377%257D%3B%20lt_timeout%3D1%3B%20lt_session%3D1%3B%20_d_id%3Df6235286-8a76-49e4-9c8a-1c9c91f4359a%3B%20bm_ss%3Dab8e18ef4e%3B%20bm_s%3DYAAQCCkSAkwnKZCXAQAAWC5DwAMOa9Au6Tagn6cLefoPegVu18dTdbi0UlULD5BUsBG%2BNL4UgoOwRgFSfdnhCMc2xHmBLIcAW7ZFpbDqDA0yjhbe7b9b06iWckv8NY48vTMPmzXUyaD3zJbwZE76SU16FERNLPAHUHWZA8789BOfXJwhanC4XFYJT2EqgmENRWOyP%2BGl5FMdpGqpfZ%2FfCtYnDojFlA0ozM3EZYfAfuoZwRUX%2B%2FGP7e8m%2FQndRCQOnuyUQ6FyzQhrASqdPcLE9AWY%2F1SohcQ%2BApos7KwiDWTessaSqmOelScIuF1OQo7%2BBbMIBWm30FrtAdiBsEAlkxeO8epOEx0%2FUM%2FOSZbfoXgO%2FAh%2B05MQb5PDZJ0%2FBXZppM4QSJRE7wYQZJNX%2BJBDmOKiN36a%2FbvVEnIaUI6PTpZ%2FS6JqNcCxbXqkbD0%2FCY51GmJLMTPPCzLU952cUT53XErIelHHHXLinhPrp4mi77ajfI%2BoccSsIJH%2Fh6ldal2rOeTtcFQvGjgHHzJWAWbn%2FAiUkfWWIzOn2TiSIKB8wkyO3XrS%3B%20bm_so%3D053A5C294108A2B0E3FB10E1958512302E95125B80BE3638E2F3F6BD4B234A1A~YAAQCCkSAk0nKZCXAQAAWC5DwATitvhxQ%2FVjXedAXFflkUxSO1SnxVKB9vDC6zQ2kpdHaVsTnbmYoUY%2BBka7JzRcPH0PEM5gLMoO9VuUt0sPxg2b4Ukc3s905Fb5vcKmsiSd8igadRyCf6xzXosvRbIBC4IBvUrzKUYueELzDpr1TWNuTFv2dcNat3em6pIg456FETJ%2Fr8im1zLCnSYIo3C2sKZap%2BhADC473ub2k9hTxQrQBJMhztKPTCX0qJ72E29nw4eSOd6K5%2FmuBxBul4WxVyhXvHexBGEbK4W6MBzWMFO1K5VeeFLNjGEFRUP8LlnmYdVycwA%2FTniNKNUu5jKLr6qmuhkQDvT5u6KkV7NZNRuHV5u%2ByeEfMAMCdnrVQ1OzM9rZGnUe92%2FbWXcZq3j4alpNOOaGg8V4xjdHCbYCaAOpOup6Vssd6c8bdemjXBfN%2BvUJ1r3ATY%2FAS3A%3D%3B%20bm_sz%3D3C68FF1FDED0D0BDA678C8D0A04E5BD0~YAAQCCkSAk4nKZCXAQAAWC5DwBxHmDwhL%2Bihjl0Rbnxip9ves1G%2BsF6MoHAHLUC2gX%2Fy%2FAqzXA4%2F1KU1U6i1P8i0AODEKACM8gsTJzJXd%2BJerNrM%2BGCdDGRI6eGqtj0Eu7TGZ9C%2BrwzYaAs7T%2Fmsw7FbnfI4gh%2BKzC0Cl0%2F2Opv8ZTOV6EYsKdbiAzSmxaJUmVulWHBZjS%2FIZv6FyTZc3JrDTRUgvDVZCn0ua1ACdkET8u0vnH9c5gxOsx8u0nyyDr4Pk%2F2UHK1r3xTV6Or2W%2B05Da%2BFQ6xb7EiTSaHDnzdFjDw%2B%2FN2YP2jtmgtZZniL48r0EUlYy4Zgu16KeqM0S77PVrYguBSYdu0YEBD%2FL%2Fp5RTG6c66On%2FDX%2BpmWrUTFxK8tfDUaOZPYKSjvyl4%3D~3290928~4272451%3B%20_mxab_%3Dconfig.bucket%253Dregular%253Bcoupon.cart.channelAware%253DchannelAware_Enabled%253Bcart.cartfiller.personalised%253Denabled%3B%20ak_bmsc%3D80C6796825284C3B58263767A9556F51~000000000000000000000000000000~YAAQCCkSAlEnKZCXAQAAJTBDwBx9RHG1Iwv5T07487juhN1t5DxBPPbReP2uA3cYfDgxUDh4Z5RJR0z3P7PcP1%2Fu39ZMKFYoBfDohLxpNnxBphX69s6LkvbjxZCkKl6RjzLxetAspZ8vg6p3Umg4Zh8s2yTle6CS3GbPa3OEfJG%2BATw544KSbj24t%2FzIduil5lQJPo8i7QicMqjwxNNtY6e95%2BNoO79s9PApQKP5zwcXb5L8v8FLRiN7jrClyDQzNPH2W4%2Bf%2BFopmeOM0LmxOvm7YJdcWAwzbzmhiQwhwU0%2F%2BSMDrck3OexdE6wiYkIO88vkE5aAlk6rM%2FxpYFOX04F43bWxZvedmWW5x2F%2F890I7q1c9IYQoCFJR%2BExFXKTrZww9pWTPvCJ%3B%20ak_RT%3D%22z%3D1%26dm%3Dmyntra.com%26si%3Dd809f49d-200d-4ea5-9963-91174d1995a5%26ss%3Dmcixapwd%26sl%3D0%26tt%3D0%22%3B%20_abck%3D5156F49879ADB44757D72DF157EB97F1~-1~YAAQCCkSAlMnKZCXAQAAZzJDwA5qUfPji65dNpEwLWVYljtHFJQ9yMKaOvpVkiVTG%2BK2cBU3Sbub%2F8Heqpmuv9GaJiQolzrLU%2FIImccJIexhCqUrgabsxn5lZONl2LDHHxh%2Bs9UMjGs9y1TkMM24yPvhFh4nIREPOvixKEk%2BD83TzzPNipbwmZwDs%2B%2FLKMzND6NsRa7WWziV003gXLa%2FqTkgKJJ9k77mBG%2FVo7H0YYBEGfxRf3%2FYFX0ipCONywnGEHcdiOcI7eOBeuE%2BhVcd4UM4QTHiyfZsXxc7uAmpXMTENe5fXqLTBjyT3a1fqvT2B0jdE%2B7A3KtPFkyTbKtNJ%2FyC%2FgnVuK2hLShXOodRHgxGnDVt28UwwZBKGSPGaQkNIVem5ACwnNEGdDIom9YDIeMUfRBhnXckJKzFnz7Ju5gdxAZTaMVIdrj462PGbHPJunsvjPKJC7y5M1yUa2YU42VaanNfQEGqYZMvZCYKFqM5GQWDys3jwh%2BSp1hxf7ti2Bfr3hn9vFLi4w%2BwQRPLgc%2B7nmH%2F1WYDR0iZs8M%3D~-1~-1~-1%3B%20mynt-eupv%3D1%3B%20bm_lso%3D053A5C294108A2B0E3FB10E1958512302E95125B80BE3638E2F3F6BD4B234A1A~YAAQCCkSAk0nKZCXAQAAWC5DwATitvhxQ%2FVjXedAXFflkUxSO1SnxVKB9vDC6zQ2kpdHaVsTnbmYoUY%2BBka7JzRcPH0PEM5gLMoO9VuUt0sPxg2b4Ukc3s905Fb5vcKmsiSd8igadRyCf6xzXosvRbIBC4IBvUrzKUYueELzDpr1TWNuTFv2dcNat3em6pIg456FETJ%2Fr8im1zLCnSYIo3C2sKZap%2BhADC473ub2k9hTxQrQBJMhztKPTCX0qJ72E29nw4eSOd6K5%2FmuBxBul4WxVyhXvHexBGEbK4W6MBzWMFO1K5VeeFLNjGEFRUP8LlnmYdVycwA%2FTniNKNUu5jKLr6qmuhkQDvT5u6KkV7NZNRuHV5u%2ByeEfMAMCdnrVQ1OzM9rZGnUe92%2FbWXcZq3j4alpNOOaGg8V4xjdHCbYCaAOpOup6Vssd6c8bdemjXBfN%2BvUJ1r3ATY%2FAS3A%3D%5E1751277318839%3B%20_ma_session%3D%257B%2522id%2522%253A%2522a4d22ca0-82ec-4bb8-bc58-f877de01fc06-f6235286-8a76-49e4-9c8a-1c9c91f4359a%2522%252C%2522referrer_url%2522%253A%2522%2522%252C%2522utm_medium%2522%253A%2522%2522%252C%2522utm_source%2522%253A%2522%2522%252C%2522utm_channel%2522%253A%2522%2522%257D%3B%20microsessid%3D441%3B%20utrid%3DAG0BcEhVVGJnZx9%252BTUtAMCMzOTkyNzcxMjkwJDI%253D.9d826a9d2129e0a8c31a82cb301704aa%3B%20_xsrf%3DJBYJqOOIFAQsKeiwn3Hi4mc1DH76CnYM%3B%20user_session%3DVfxSOH5PKKQhaYeB9Rv4Kw.SG-3w-gacKhHOpIYIlMN3YZbWQbn4oNkZJzTVNiSeaxd6FelEmy2Kv_bl9qOYYBVTpS33fewO6W6dRrOohsaY7_xcyFEI5CmVJgrEnb_Vm3mPx2CE15hKtptGow5-wLXErQgI8jmLeKzeZinASyclw.1751277319112.86400000.3JN_gZbdGGmHmMdCe-cp4Y4y5o6DjEKROju-O8aVUDA%3B%20bm_sv%3D6354575938FE6F160E911BA95E1D1EE9~YAAQCCkSAlQnKZCXAQAADjRDwBzw%2Bg1UWq8wTNMIeYPtePE5Aj6Uyp72eLkPuqvjN5GZ%2FOs1CGE04FBQ%2FnRIqvTV4KaR8wjgbnCE3am2uPX2wCxdxSFmdvAmDL4cYb6nkDRzCcNfd7oHhnZWOhB%2FQy6ZBvwV0B26wIJXgyDhtMW9iO0oVGK9q2GPiHDMVrZaUpwUl2zz%2Bg293z37nH6U1HD9qcbhcwqIAPMc4hCCeY030v4XZ%2B8jueY622I8HLn5~1"
            response = requests.get(url)
        else:
            response = requests.get(
                url=f'https://www.myntra.com/gateway/v2/product/{pid}/related',
            )
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Request failed for URL {url}: {str(e)}")
        raise


@with_backoff
def get_review_response(url):
    pid = extract_pid(url)
    url = f"https://www.myntra.com/reviews/{pid}"
    try:
        if PROXY_MYNTRA:
            response = requests.get(
                url=url,proxies=PROXY, verify=False
            )
        else:
            response = requests.get(url=url,)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Request failed for URL {url}: {str(e)}")
        raise


if __name__ == '__main__':
    respons_text = get_pdp_response(url='https://www.myntra.com/31382776')
    print(get_data_pdp(respons_text, 'https://www.myntra.com/31382776'))