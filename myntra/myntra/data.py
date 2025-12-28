import json

import requests
from loguru import logger
from parsel import Selector


def get_links(cookies_, headers_, keyword, url):
    list_of_links = []
    response = requests.get(url=url, cookies=cookies_, headers=headers_)
    selector = Selector(text=response.text)
    json_data = selector.xpath("//script[contains(text(),'searchData')]/text()").get()
    if json_data:
        json_data = json_data.replace("window.__myx =", "").strip()
        json_data = json.loads(json_data)
    else:
        json_data = json.loads(response.text)
    results = json_data.get('searchData').get('results').get('products')
    if not results:
        results = results.get('products')

    if results:
        for index, result in enumerate(results):
            # Todo: Break Loop If Index Count: 25
            if index >= 25:
                break
            index += 1

            item = dict()
            product_id = result.get('productId')
            product_url = result.get('landingPageUrl')
            if product_url:
                product_url = f"https://www.myntra.com/{product_url}"

            # Todo: make item fileds
            # item['keyword'] = keyword
            # item['product_id'] = product_id
            # item['product_url'] = product_url
            list_of_links.append(product_url)

        print(len(list_of_links))

        # Todo: make requests if results(Product Counts) length < 25
        if len(results) < 25:
            cookies = {
                'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pWVRnek1EYzNNemd0TlRGaVl5MHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZME1EVXhNVFlzSW1semN5STZJa2xFUlVFaWZRLnN5aFcwTHJtdy1LQlRwR2hoU2Z2b1JMUmZmTDRDSDdNaU1remF0MTFUQlE=',
                'lt_timeout': '1',
                'lt_session': '1',
                '_d_id': '110e2c85-58a4-4dbe-9301-20ae21870966',
                'bm_ss': 'ab8e18ef4e',
                'bm_s': 'YAAQSs4tF6A6K3yXAQAASGT6pgNTyQ5scnNRaWzsBdQkPbjmGXU3wbZOz5Sp+uu/iMQKf+8bAE5zfLcEz0kCRtDKWekUoOZwTVIdPpbZfTbkkY6XRi0mLwBDpOLctF7H9P+d0uQGhoe+TvYZs2gISHy/KBtdeGHgcVpB8Ejh01BqXoqoJi7Jp9KUH0SRlcjVQcbSXQeGP9S7Mnx96kcE6mDC4bpFTVNNWVVKDx+k6pCeXb9j23Uu81soVZie2EZs5ay5/rJBqiBScvkI3gtwQW3KAbjxFn5Vra66GvBpGa/06C3RQulx1GTBPC2mckUPWSu/ZgKsQhDLzFOM+1lyrAi3tjq71lzn6eXeJfwi9mkv7+J54tREluLMQHTMl4FyTwdRpDFkmeJLTYnXSDDahX5jiFQFuQX/6NbyF+z2f50Y8U3X96eY5BWESTxEFCj5bsqKlNM4ye0ALgnHnAa1hIvn8ivA9zaMhv0ENX8kCcDoH9TgMAju/G75bft0eMXjqZAPTqraA2uRaCX3arwr4T4ZSnUy94jDxILQZg9zLFYymuJZ4KJw',
                'bm_so': '8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=',
                'mynt-eupv': '1',
                '_mxab_': 'config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled',
                'microsessid': '665',
                '_xsrf': '0JJscjS4YERWw58YPlwqOLLEb4843MNH',
                'bm_lso': '8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=^1750853121030',
                'mynt-ulc-api': 'pincode%3A380001',
                'mynt-loc-src': 'expiry%3A1750854561369%7Csource%3AIP',
                'ak_bmsc': '9B17AA5F63EF7FEBE0CDFE4E8A62E889~000000000000000000000000000000~YAAQSs4tF4Q7K3yXAQAAdnX6phy4aGlyovUWccQG+8uS0qNWkYps/GCOUCQ8vRESKHB/57LE2MgIMYGtzAlot3eTFOkIVUXDe40NOGivT5d1bLABy3E5dzIAZl7e38Yt9JR4ypvfzDut7WaYOVlwNSWB1N518TfPz0FwJg1bRiGlEUz5vXr/KLmUhP/0Pu1PR57Np0xkyg06i3Ph566Up2w+r5NIvpqo2LrTrpTfUsDtuy5CDfSbKrDWzd2ekd72Y81eBEcA9ZqKYq8bjQy65HJHf78NMw5eYirX7Lyn9v4ld+v76FUYba0z5JwW1cgKGclk8ujRwyF0EZHTfzRUakn1zNgFub7R3W17BlxMpLO8pqeMWOhxGIsor9I25bxvOHR8yAc172uVEv+X50AYBUkH1ZGWPu7SHrtoLAj/bLJZ6znZul4ewQyCB7CMSFPRVFRaALQOvLeZQJA/',
                '_gcl_au': '1.1.650218370.1750853122',
                'x-mynt-pca': 'f1ndLPB9m7Kj9HabABct0F8en18USiopZzWWd40h0ee-1Uw2ErbNYm1cg7_f5wBJssSndWpI2q59UqKLIweE6-l5KQqG7cbdimztU-XF9fbYPzfAMhd6de19qf3J28DCuHTS_PsGVtbM7wm6eWDLQJzkqyLQ-GMu71IjvPO8hEKeefT_3e717w%3D%3D',
                'tvc_VID': '1',
                '_scid': 'x2cwiqJo0xSTmZVV3KAe5dF8_AlVkJGx',
                '_cs_ex': '1',
                '_cs_c': '1',
                '_fbp': 'fb.1.1750853123203.929586668242512692',
                '_ScCbts': '%5B%5D',
                '_sctr': '1%7C1750789800000',
                '_abck': '20DCFFB6096F390F279FD729F4F28671~0~YAAQRc4tF4nFroOXAQAAFJD6pg7TdLACUWQrCai8+TlBUEXiyc+0KiNzMHIYHXAzSk4ywIeGjU7Mk9Q9pA1VRNmegQlXmxvCvhbp4ks7OW39gHB1yFNvQp2DrMTptzuGpjBVKSXt/yDh63huE6aPdi3NflYNOgOvgHBA/A+OT5nAAJQGpLh2m02lvl3aMLKyxX2Dg3v8hVNUxapQHEKc7KWJSY0dWSHDuHXb3LfYPrZKS/rTcCqzTlb13vWh6Lbtib8FWcKFyFM/uDDJ1VCuEwJnkXnb9ZtkaseFHdTRBom39L23HQwJkknm74KkDtiCCgkYr166oDD0QaDHQIiTWQory4KE1VU3Y4ivwk+0xDBscyn0D7/J4ljvARhIMgSCG4HxBGkGpSGmVUbKEJT1rvEQJzmDUAqyTFcHUcWlFT5tQnzhbiEiZuq6Lv970JgUUBhWpg7Kv0BbmTyWEP0N1gRH4zEbKSLFO3qjYLo0JZxwDcJtbawlIqEayJ4qePu2V793SkftcNDfs/IXoZASYxr7fVBgK5wh8rlPS4TcqvzVotek1t17JxDQWXpN9A7vMRV6fkKfIzYwSRFWrt8iZGXgKTohjeeQMCUFckXIa2me7z3SyVp+f/XdZp55~-1~-1~-1',
                '_ma_session': '%7B%22id%22%3A%22fb2116b0-47b6-4a24-8f09-dbe92dde4266-110e2c85-58a4-4dbe-9301-20ae21870966%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D',
                'bm_sz': 'B6E993881B0953753EDE09764AFC253C~YAAQSM4tF+CW4IOXAQAAchz7phxzu2RDvrV2WGUW+suiGyV96SZIYTZ5uZwiKUf3kGK7yopU7s2FpC0U/dAW571RdQsE7GKa0pvVjqGAJquqihQ91ls+Zvy3ZGZgXePTJTr+mMw6byj45ZrvTugrzjs3Gxf45Y85Y7hJNhi3hjGQ84U1N/jHf8VYw257WquZ4Ab7EDTQmgk5TIooLDFF+3uoVhGn3S1w6hxjlUm7DuOnIvEyrxgSkZtV4HDFqiPsJQzw9jK8EPuH+n6AjNQBVsRsvnpZdz6vie3lbNLbiW7u82cDhRA0XT9ID+RtosFNMEj9MHpdspwwhyfTxwteqygrzap4fxLuU2s8a4Hs5imrnbiI2Nx4vXY3AkYzf36eGeO+cUp8j8juPMyfNVKjr72oOSrq9/9nHpsz~3158082~4408901',
                'ak_RT': '"z=1&dm=myntra.com&si=0f4d4fff-b049-41a8-9a0f-3782fd5b439e&ss=mcbwqlt1&sl=2&tt=7ur&obo=1&rl=1"',
                '_scid_r': '0ecwiqJo0xSTmZVV3KAe5dF8_AlVkJGxl5grJQ',
                '_pv': 'default',
                'dp': 'd',
                'utrid': 'R2B%2BRQ5TG1YYBUZDC0tAMCMzMjU3NTI5MDk1JDI%3D.40f16deaaf87366d4d478ec7bcc6c0fb',
                'bm_sv': '64071DE2050E96B4F20E5A3B026F3B2A~YAAQbw7EF6/nCXuXAQAAI+cOpxzt3MtPZSer4AMWrOuJDdptJq5j9JEsFa92jRlm5kd76NgDqw84aig/sigxwVRG9oQmgQ/Mh3/V4YVMMFTTc/dLITuDhzQWiQYu+HXBjh7fhzryf2rcDWSVqCtXMUxXV+484aqgytdGeAi00G2Y5o6rjWdn7VHwVlQuTSMLvzRWwoFRbfKyrAGjzJ7sTTUYaRcnF1sKGugHpqaVbIwFoYxGbkxvIApG3tXuofhspg==~1',
            }
            headers = {
                'accept': 'application/json',
                'accept-language': 'en-US,en;q=0.9',
                'app': 'web',
                'content-type': 'application/json',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwNjIwNzEiLCJhcCI6IjcxODQwNzY0MyIsImlkIjoiNjA4OGM5MzExNWIwMjJjYSIsInRyIjoiZGZlNjVmNzkyN2U5NjI0MDk5MGY5NTRjYjc1OGU5M2EiLCJ0aSI6MTc1MDg1NDU3ODA4NCwidGsiOiI2Mjk1Mjg2In19',
                'pagination-context': '{"scImgVideoOffset":"0_0","v":1.0,"productsRowsShown":0,"paginationCacheKey":"1fdfa418-9b8f-4fa6-8a60-93972510090d","inorganicRowsShown":0,"plaContext":"eyJwbGFPZmZzZXQiOjAsIm9yZ2FuaWNPZmZzZXQiOjMyLCJleHBsb3JlT2Zmc2V0IjowLCJmY2NQbGFPZmZzZXQiOjUwLCJzZWFyY2hQaWFub1BsYU9mZnNldCI6NDcsImluZmluaXRlU2Nyb2xsUGlhbm9QbGFPZmZzZXQiOjAsInRvc1BpYW5vUGxhT2Zmc2V0IjozLCJvcmdhbmljQ29uc3VtZWRDb3VudCI6MTQyLCJhZHNDb25zdW1lZENvdW50Ijo1MCwiZXhwbG9yZUNvbnN1bWVkQ291bnQiOjAsImN1cnNvciI6eyJUT1BfT0ZfU0VBUkNIIjoiZmVhOmt3dHxpZHg6M3xzcmM6RkNDfmZlYTpua3d0fGlkeDowfHNyYzpGQ0N+ZmVhOmt3dHxpZHg6MHxzcmM6TVlOVFJBX1BMQX5mZWE6bmt3dHxpZHg6MHxzcmM6TVlOVFJBX1BMQSIsIlNFQVJDSCI6ImZlYTprd3R8aWR4OjQ3fHNyYzpGQ0N+ZmVhOm5rd3R8aWR4OjB8c3JjOkZDQ35mZWE6a3d0fGlkeDowfHNyYzpNWU5UUkFfUExBfmZlYTpua3d0fGlkeDowfHNyYzpNWU5UUkFfUExBIn0sInBsYXNDb25zdW1lZCI6W10sImFkc0NvbnN1bWVkIjpbXSwib3JnYW5pY0NvbnN1bWVkIjpbXSwiZXhwbG9yZUNvbnN1bWVkIjpbXX0\\u003d","refresh":false,"scOffset":0,"reqId":"1fdfa418-9b8f-4fa6-8a60-93972510090d"}',
                'priority': 'u=1, i',
                'referer': f'https://www.myntra.com/{keyword}',
                'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'traceparent': '00-dfe65f7927e96240990f954cb758e93a-6088c93115b022ca-01',
                'tracestate': '6295286@nr=0-1-3062071-718407643-6088c93115b022ca----1750854578084',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-location-context': 'pincode=380001;source=IP',
                'x-meta-app': 'channel=web',
                'x-myntra-app': 'deviceID=110e2c85-58a4-4dbe-9301-20ae21870966;customerID=;reqChannel=web;appFamily=MyntraRetailWeb;',
                'x-myntraweb': 'Yes',
                'x-requested-with': 'browser',
                # 'cookie': 'at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pWVRnek1EYzNNemd0TlRGaVl5MHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZME1EVXhNVFlzSW1semN5STZJa2xFUlVFaWZRLnN5aFcwTHJtdy1LQlRwR2hoU2Z2b1JMUmZmTDRDSDdNaU1remF0MTFUQlE=; lt_timeout=1; lt_session=1; _d_id=110e2c85-58a4-4dbe-9301-20ae21870966; bm_ss=ab8e18ef4e; bm_s=YAAQSs4tF6A6K3yXAQAASGT6pgNTyQ5scnNRaWzsBdQkPbjmGXU3wbZOz5Sp+uu/iMQKf+8bAE5zfLcEz0kCRtDKWekUoOZwTVIdPpbZfTbkkY6XRi0mLwBDpOLctF7H9P+d0uQGhoe+TvYZs2gISHy/KBtdeGHgcVpB8Ejh01BqXoqoJi7Jp9KUH0SRlcjVQcbSXQeGP9S7Mnx96kcE6mDC4bpFTVNNWVVKDx+k6pCeXb9j23Uu81soVZie2EZs5ay5/rJBqiBScvkI3gtwQW3KAbjxFn5Vra66GvBpGa/06C3RQulx1GTBPC2mckUPWSu/ZgKsQhDLzFOM+1lyrAi3tjq71lzn6eXeJfwi9mkv7+J54tREluLMQHTMl4FyTwdRpDFkmeJLTYnXSDDahX5jiFQFuQX/6NbyF+z2f50Y8U3X96eY5BWESTxEFCj5bsqKlNM4ye0ALgnHnAa1hIvn8ivA9zaMhv0ENX8kCcDoH9TgMAju/G75bft0eMXjqZAPTqraA2uRaCX3arwr4T4ZSnUy94jDxILQZg9zLFYymuJZ4KJw; bm_so=8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=; mynt-eupv=1; _mxab_=config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled; microsessid=665; _xsrf=0JJscjS4YERWw58YPlwqOLLEb4843MNH; bm_lso=8F246ECE2561D23A0BD0F787DF22DF10BD19DAC645F4ABBDF4A7EAB00DE6A479~YAAQSs4tF6E6K3yXAQAASGT6pgTt8952lX5RztpMuISajJRtQsfqRYSDAjCE3/Iad5nezN6nSjCQxPxIRQI/CKOM3GtgHKvBvxCGLCMLEvRIp5RGh6ADE29l8N33BLx+43k1Yok8U8cazpHRMW+Ij2xe7uuY6JBKpHyAGJ80gPUAwUJQl6ZlkkE7weF5upJbfyvsR/CfZbiW2dJOctRKbs1nqGXQr9ocIDEaJvph+0kIiXIzMfAXj1ZGv5ZNRKduvwwtY+/Z6+RfeM5HFOUusvgkzo5ic02v1ZU3o0Z8U+Nudxj8PueqGxowlZNwDazhLmAf4nbnaJ6W6GEVhWgsrkDHgVM8LYYAsgvcdQNK2YBB4xpcB4SakAZ+bnTIMW2iXJwjTJ+sG/pHhl/zZ6x9mtbm4fYMm26T0AjuyOS5Hli+3O9K+mugBvV3/FOfj4ltm7LBbZCpi1dt+FmKmZU=^1750853121030; mynt-ulc-api=pincode%3A380001; mynt-loc-src=expiry%3A1750854561369%7Csource%3AIP; ak_bmsc=9B17AA5F63EF7FEBE0CDFE4E8A62E889~000000000000000000000000000000~YAAQSs4tF4Q7K3yXAQAAdnX6phy4aGlyovUWccQG+8uS0qNWkYps/GCOUCQ8vRESKHB/57LE2MgIMYGtzAlot3eTFOkIVUXDe40NOGivT5d1bLABy3E5dzIAZl7e38Yt9JR4ypvfzDut7WaYOVlwNSWB1N518TfPz0FwJg1bRiGlEUz5vXr/KLmUhP/0Pu1PR57Np0xkyg06i3Ph566Up2w+r5NIvpqo2LrTrpTfUsDtuy5CDfSbKrDWzd2ekd72Y81eBEcA9ZqKYq8bjQy65HJHf78NMw5eYirX7Lyn9v4ld+v76FUYba0z5JwW1cgKGclk8ujRwyF0EZHTfzRUakn1zNgFub7R3W17BlxMpLO8pqeMWOhxGIsor9I25bxvOHR8yAc172uVEv+X50AYBUkH1ZGWPu7SHrtoLAj/bLJZ6znZul4ewQyCB7CMSFPRVFRaALQOvLeZQJA/; _gcl_au=1.1.650218370.1750853122; x-mynt-pca=f1ndLPB9m7Kj9HabABct0F8en18USiopZzWWd40h0ee-1Uw2ErbNYm1cg7_f5wBJssSndWpI2q59UqKLIweE6-l5KQqG7cbdimztU-XF9fbYPzfAMhd6de19qf3J28DCuHTS_PsGVtbM7wm6eWDLQJzkqyLQ-GMu71IjvPO8hEKeefT_3e717w%3D%3D; tvc_VID=1; _scid=x2cwiqJo0xSTmZVV3KAe5dF8_AlVkJGx; _cs_ex=1; _cs_c=1; _fbp=fb.1.1750853123203.929586668242512692; _ScCbts=%5B%5D; _sctr=1%7C1750789800000; _abck=20DCFFB6096F390F279FD729F4F28671~0~YAAQRc4tF4nFroOXAQAAFJD6pg7TdLACUWQrCai8+TlBUEXiyc+0KiNzMHIYHXAzSk4ywIeGjU7Mk9Q9pA1VRNmegQlXmxvCvhbp4ks7OW39gHB1yFNvQp2DrMTptzuGpjBVKSXt/yDh63huE6aPdi3NflYNOgOvgHBA/A+OT5nAAJQGpLh2m02lvl3aMLKyxX2Dg3v8hVNUxapQHEKc7KWJSY0dWSHDuHXb3LfYPrZKS/rTcCqzTlb13vWh6Lbtib8FWcKFyFM/uDDJ1VCuEwJnkXnb9ZtkaseFHdTRBom39L23HQwJkknm74KkDtiCCgkYr166oDD0QaDHQIiTWQory4KE1VU3Y4ivwk+0xDBscyn0D7/J4ljvARhIMgSCG4HxBGkGpSGmVUbKEJT1rvEQJzmDUAqyTFcHUcWlFT5tQnzhbiEiZuq6Lv970JgUUBhWpg7Kv0BbmTyWEP0N1gRH4zEbKSLFO3qjYLo0JZxwDcJtbawlIqEayJ4qePu2V793SkftcNDfs/IXoZASYxr7fVBgK5wh8rlPS4TcqvzVotek1t17JxDQWXpN9A7vMRV6fkKfIzYwSRFWrt8iZGXgKTohjeeQMCUFckXIa2me7z3SyVp+f/XdZp55~-1~-1~-1; _ma_session=%7B%22id%22%3A%22fb2116b0-47b6-4a24-8f09-dbe92dde4266-110e2c85-58a4-4dbe-9301-20ae21870966%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D; bm_sz=B6E993881B0953753EDE09764AFC253C~YAAQSM4tF+CW4IOXAQAAchz7phxzu2RDvrV2WGUW+suiGyV96SZIYTZ5uZwiKUf3kGK7yopU7s2FpC0U/dAW571RdQsE7GKa0pvVjqGAJquqihQ91ls+Zvy3ZGZgXePTJTr+mMw6byj45ZrvTugrzjs3Gxf45Y85Y7hJNhi3hjGQ84U1N/jHf8VYw257WquZ4Ab7EDTQmgk5TIooLDFF+3uoVhGn3S1w6hxjlUm7DuOnIvEyrxgSkZtV4HDFqiPsJQzw9jK8EPuH+n6AjNQBVsRsvnpZdz6vie3lbNLbiW7u82cDhRA0XT9ID+RtosFNMEj9MHpdspwwhyfTxwteqygrzap4fxLuU2s8a4Hs5imrnbiI2Nx4vXY3AkYzf36eGeO+cUp8j8juPMyfNVKjr72oOSrq9/9nHpsz~3158082~4408901; ak_RT="z=1&dm=myntra.com&si=0f4d4fff-b049-41a8-9a0f-3782fd5b439e&ss=mcbwqlt1&sl=2&tt=7ur&obo=1&rl=1"; _scid_r=0ecwiqJo0xSTmZVV3KAe5dF8_AlVkJGxl5grJQ; _pv=default; dp=d; utrid=R2B%2BRQ5TG1YYBUZDC0tAMCMzMjU3NTI5MDk1JDI%3D.40f16deaaf87366d4d478ec7bcc6c0fb; bm_sv=64071DE2050E96B4F20E5A3B026F3B2A~YAAQbw7EF6/nCXuXAQAAI+cOpxzt3MtPZSer4AMWrOuJDdptJq5j9JEsFa92jRlm5kd76NgDqw84aig/sigxwVRG9oQmgQ/Mh3/V4YVMMFTTc/dLITuDhzQWiQYu+HXBjh7fhzryf2rcDWSVqCtXMUxXV+484aqgytdGeAi00G2Y5o6rjWdn7VHwVlQuTSMLvzRWwoFRbfKyrAGjzJ7sTTUYaRcnF1sKGugHpqaVbIwFoYxGbkxvIApG3tXuofhspg==~1',
            }
            next_page_url = f'https://www.myntra.com/gateway/v2/search/{keyword}?rows=50&o=49'
            get_links(cookies, headers, keyword, next_page_url)
    else:
        logger.error("Product Details Can Not Found")


if __name__ == '__main__':
    cookies = {
        '_d_id': '0a039ed9-c93d-4316-87cc-5227cf36b441',
        'at': 'ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTm1VMFpUazJOamt0TlRFNVlpMHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZek9UQTRORFlzSW1semN5STZJa2xFUlVFaWZRLkprRHdqN0lWQmxHRkcxY05ybkhCX25BelFLMjBqa2YyNHFZb2p2MURwYU0=',
        'mynt-eupv': '1',
        '_gcl_au': '1.1.1443091708.1750838847',
        'x-mynt-pca': 'dMfMXwZKNndyCg-wRllPxqDqrfnbwd95e5y77JwtSIdlyq-_AfqJznJdsG5JdAANYf1nEp4kY6iMPM2boBREdopvooDWzX28DIf2yWYa-5aUBhRbvilZE08_v-C4CZwNQMwnR45UAPop62k4F6wE3c5sZcFkI1oI2a8qQ_Oisj6GWYeX6WO_SA%3D%3D',
        '_scid': 'OG_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPWA',
        '_fbp': 'fb.1.1750838847780.512220360261025021',
        'tvc_VID': '1',
        '_cs_ex': '1',
        '_cs_c': '1',
        '_ScCbts': '%5B%5D',
        '_sctr': '1%7C1750789800000',
        'mynt-ulc-api': 'pincode%3A380001',
        '_mxab_': 'config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled',
        '_pv': 'default',
        'dp': 'd',
        'lt_timeout': '1',
        'lt_session': '1',
        'bm_ss': 'ab8e18ef4e',
        'microsessid': '64',
        '_xsrf': 'cD1EqFwOYHU0CPGuc3ijVX634sELCWnL',
        '_ma_session': '%7B%22id%22%3A%225426b4ba-97af-4973-b965-ba41b8188366-0a039ed9-c93d-4316-87cc-5227cf36b441%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D',
        'mynt-loc-src': 'expiry%3A1750918411095%7Csource%3AIP',
        'ak_bmsc': 'A2F32B1845B5FDBEF5DC96F864074F94~000000000000000000000000000000~YAAQdA7EF5187aSXAQAAcbrIqhya4A6S8nxqXsNpjmx/cR84wdSRv/YZYDE/1EkE3Ih2N+RTueVLk7hfn0+CDgxHp0YqyZFB9eoAv7woLqV92uU4Z3STYg5FMCUtqV5uGEo0Py83HTbFmxXk8ba2I9GQsVT5wpfznHNMxVJDk9ZOzaZbtYcYsALTI0XlmsRI3tDafDV86BHSGwTNRXMdauJK3pW2Th918Tn5hx1bLbdn1uVKdj68abPhUb6nkysVymlFyxFu1UUCUzALBVG9PPMA12F1KBPFkPoEYkmNj49+cuyP2eN66h7Txbpffg38mRWc1TvdZKXvuTIGhgcwpqldyqre0WiJxKY5t7mLfsB77H3CqR+YMcaPPATfgQZdIYlUIHQJhwmgX4dF8xI3LZA/Qs291/ZyEyARYHC2JO+X8nVwBf67kE2Sh0HbgSlkszIUl36+Cc7D62/t',
        '_abck': '24639F7CCD89A18F081F73A07E70E269~0~YAAQRA7EFyfGqIyXAQAA7ujIqg460uGuGYTWWKVgtON9/Zk7iG0eA7ZuBdkkBZCXvdyc7svuRf+witD+bXtH4+ukLrRvBJPiST1TldZIHWs/nGy7hL4FEXR35rpzEIf+ejWIPAYSzkBoowDDKbXMalk73ieNCyJs2FHNbULz4CWQtmutlxkd80ze40qCi0DJ6toTwqpp4B9oaRDVjpvJJHOnQaLN4PqAAHJQpMlF+uEvOXsU5KjyLrOmAs1h1pup//jgewBd0km5QNTZOHVXkb9zXqyehlWJAWIwDvAuQN0z6o4P84IiPbU5uhT+dj4FUyAfLFhfVlQYksa5dx/yh9EGjzLwoCjGJQiw5MLEmcPvuPYQSutWum+jtWJrT6VV27f4Zl8DdIF/h0UxTp1VjDZwoHk19OWNzeyz9DmJX48c9T8Fr6Mr2pTdDyr98uEwkvJvp82HZzzEG7OSScUWFyglJfEZspbJMDp4WbXJ48Wi3/l9hPufpAtfxOUjAHp2x2GdembTLib2uHykhPZpsg/2DqqMWZdLPt2LBzp9UTV2msckQ3OpXTRNv4i4AkzECE/sJzSGQLfubcJ0ky30O4rxmIPIoIYs0n0nLLiEYsS1geWtelia3y7TQhAv~-1~-1~-1',
        'user_session': 'fuwOxZ7Mkhcte-08UImXWw.6_ozKKUTXSUg1PutRt_ruqt_1tTOVaAYxrSFOyIBzTOTk8z7qXOYnDHjaV1nBPPv4R5Swck2l2JD0I9sWzP2qGXDpqTmpsixZQBDxAox8HzGSVjRElye_VDMugDV5whvQFdtC0H5yvfmR38inrzOfg.1750916970619.86400000.hlnL73fPWCuQA3YHJSpMSIECYVko_OqxfNhkuqHe4YU',
        'bm_s': 'YAAQJg7EF5e1aaiXAQAALSbJqgM9IkJGWhfqL57/TUWfikadX0vOd/lURZ/kpLiKyJA2UlXB6QWf/4C4l9sCsckkD9rgqZdJnZ/OC4EIYFPjZa2vtZOdms9ZvBTmE/ZaKsqXgPqYs/JwJ+wqpXN9AGauJmaa8nES5PbfvnXR6G2Hep1aNjitmQHMV05tMkPN3eiNqSF/uPlXN+zO+wVVxvopFmFF3iShXIyNJUcEZG6yAPQK8D1HHl/AHOs0hXcNVUI8G1YOpW0JZaG27K5QsX045UXnGzFi/CPb/OeWwNmtAoFdz1RfLh7WsLWslZFj4oLr0zcXqllPvXnulecr57HY9gnjWkYNHvuG5KY4Os6R70GhYTlaqDwa6+FdprIZ/EwlXbJ53ptAlGzoXR1H5Zat0YJT8Uo0S30fF4E6y2v1r3kGhpIlAaaBnM2v9haPVGfheRF9S017I558X7doicH4KE14FD30UJMAf+JjmboO0VvIGlQMXm4lO61snnOsjjgOa5M+3vfViCNReuARvCTOIxLhHiHEfb9XHtVzKsBl1TcSGvBqBzVsfLzLCL1+gxmhUz6f',
        'bm_so': '7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=',
        'bm_sz': '2D91F866169FB502658FB5005B0AD486~YAAQJg7EF5q1aaiXAQAALSbJqhx0iaEYUlOGz990MvdUh2uKUzYU8BpvZHtYtD0i69Why+elCNLo2tYsRTY/gZ3nGMuhHW9eDrrGAtO2uk2IyqGpmKeGXcnVNW+BKAcnE1EpzPUan/9O1zMwmT18KNlXVeYNbLxwQQAyvD8ildu1/Z0d6pw6KW+5Fu+xSRXnTGces4NOlp8Z7wuoTm3V+8Q8UJfoPSzQjXPO7QvHyII3M6Vchd8zoLM/GPfvLTHvCrjbFKOjrvWS1FEQVfLt8QP0gkOJb53I6XkWF68t3nWC5iZ+XhbMGTO+31ekerTemommXt39ljcU5AlQKpvMarKfxktZVuqtibwzEEq2uzBlqaursXYQ7h2wcStfIhxwpNKYqDLEfFlb0Hzv5MFJbuP02fUJE/Z1nENg~3359029~4403778',
        'utm_track_v1': '%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1750916999%2C%22trackend%22%3A1750917059%7D',
        '_scid_r': 'Om_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPaQ',
        'bm_lso': '7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=^1750917001091',
        'utrid': 'XW9%2FFVdicUJTam4bakVAMCMxNDg4ODc0NzIxJDI%3D.8f11f6137cc51ca0102c67c069ce4fee',
        'bm_sv': '095E1B91BE958E52491C0A14B9FFB242~YAAQJg7EFyy3aaiXAQAAtjrJqhwZcYkLk7WwVx8sAbk8+DzjneCIGnBlNpUBYBD1B0Qe+gU5cGHJPLUu72PY/9SRG6GyIzouCibzkCyFNlMTEFIznMUescbYwpM/k4YWX+KvI+ro9sJorWpFaNymtPx0HBxRmPrqFdLfH5Qt6ozOUapjZYQ7KLdY4+CVCjIOcCBzb+c1FWEd0UNWOhSfDgiRQxxIJxQmQD7DH5vZ7IVPVZ8CVYch0FXMrWOpM02AaA==~1',
        'ak_RT': '"z=1&dm=myntra.com&si=c3903ef9-b23d-431c-a0b4-2c150e2270c5&ss=mccyr7x4&sl=3&tt=1q6&obo=2&rl=1&ld=11uu&r=48oj4cny&ul=11uw"',
    }
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'if-none-match': 'W/"e7841-fYh4Hp3oIOGi1arOiXKlsowF3/4"',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        # 'cookie': '_d_id=0a039ed9-c93d-4316-87cc-5227cf36b441; at=ZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNklqRWlMQ0owZVhBaU9pSktWMVFpZlEuZXlKdWFXUjRJam9pTm1VMFpUazJOamt0TlRFNVlpMHhNV1l3TFdKallXRXRZV1UwTmpWbVpHTmlORFkxSWl3aVkybGtlQ0k2SW0xNWJuUnlZUzB3TW1RM1pHVmpOUzA0WVRBd0xUUmpOelF0T1dObU55MDVaRFl5WkdKbFlUVmxOakVpTENKaGNIQk9ZVzFsSWpvaWJYbHVkSEpoSWl3aWMzUnZjbVZKWkNJNklqSXlPVGNpTENKbGVIQWlPakUzTmpZek9UQTRORFlzSW1semN5STZJa2xFUlVFaWZRLkprRHdqN0lWQmxHRkcxY05ybkhCX25BelFLMjBqa2YyNHFZb2p2MURwYU0=; mynt-eupv=1; _gcl_au=1.1.1443091708.1750838847; x-mynt-pca=dMfMXwZKNndyCg-wRllPxqDqrfnbwd95e5y77JwtSIdlyq-_AfqJznJdsG5JdAANYf1nEp4kY6iMPM2boBREdopvooDWzX28DIf2yWYa-5aUBhRbvilZE08_v-C4CZwNQMwnR45UAPop62k4F6wE3c5sZcFkI1oI2a8qQ_Oisj6GWYeX6WO_SA%3D%3D; _scid=OG_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPWA; _fbp=fb.1.1750838847780.512220360261025021; tvc_VID=1; _cs_ex=1; _cs_c=1; _ScCbts=%5B%5D; _sctr=1%7C1750789800000; mynt-ulc-api=pincode%3A380001; _mxab_=config.bucket%3Dregular%3Bcoupon.cart.channelAware%3DchannelAware_Enabled%3Bcart.cartfiller.personalised%3Denabled; _pv=default; dp=d; lt_timeout=1; lt_session=1; bm_ss=ab8e18ef4e; microsessid=64; _xsrf=cD1EqFwOYHU0CPGuc3ijVX634sELCWnL; _ma_session=%7B%22id%22%3A%225426b4ba-97af-4973-b965-ba41b8188366-0a039ed9-c93d-4316-87cc-5227cf36b441%22%2C%22referrer_url%22%3A%22%22%2C%22utm_medium%22%3A%22%22%2C%22utm_source%22%3A%22%22%2C%22utm_channel%22%3A%22direct%22%7D; mynt-loc-src=expiry%3A1750918411095%7Csource%3AIP; ak_bmsc=A2F32B1845B5FDBEF5DC96F864074F94~000000000000000000000000000000~YAAQdA7EF5187aSXAQAAcbrIqhya4A6S8nxqXsNpjmx/cR84wdSRv/YZYDE/1EkE3Ih2N+RTueVLk7hfn0+CDgxHp0YqyZFB9eoAv7woLqV92uU4Z3STYg5FMCUtqV5uGEo0Py83HTbFmxXk8ba2I9GQsVT5wpfznHNMxVJDk9ZOzaZbtYcYsALTI0XlmsRI3tDafDV86BHSGwTNRXMdauJK3pW2Th918Tn5hx1bLbdn1uVKdj68abPhUb6nkysVymlFyxFu1UUCUzALBVG9PPMA12F1KBPFkPoEYkmNj49+cuyP2eN66h7Txbpffg38mRWc1TvdZKXvuTIGhgcwpqldyqre0WiJxKY5t7mLfsB77H3CqR+YMcaPPATfgQZdIYlUIHQJhwmgX4dF8xI3LZA/Qs291/ZyEyARYHC2JO+X8nVwBf67kE2Sh0HbgSlkszIUl36+Cc7D62/t; _abck=24639F7CCD89A18F081F73A07E70E269~0~YAAQRA7EFyfGqIyXAQAA7ujIqg460uGuGYTWWKVgtON9/Zk7iG0eA7ZuBdkkBZCXvdyc7svuRf+witD+bXtH4+ukLrRvBJPiST1TldZIHWs/nGy7hL4FEXR35rpzEIf+ejWIPAYSzkBoowDDKbXMalk73ieNCyJs2FHNbULz4CWQtmutlxkd80ze40qCi0DJ6toTwqpp4B9oaRDVjpvJJHOnQaLN4PqAAHJQpMlF+uEvOXsU5KjyLrOmAs1h1pup//jgewBd0km5QNTZOHVXkb9zXqyehlWJAWIwDvAuQN0z6o4P84IiPbU5uhT+dj4FUyAfLFhfVlQYksa5dx/yh9EGjzLwoCjGJQiw5MLEmcPvuPYQSutWum+jtWJrT6VV27f4Zl8DdIF/h0UxTp1VjDZwoHk19OWNzeyz9DmJX48c9T8Fr6Mr2pTdDyr98uEwkvJvp82HZzzEG7OSScUWFyglJfEZspbJMDp4WbXJ48Wi3/l9hPufpAtfxOUjAHp2x2GdembTLib2uHykhPZpsg/2DqqMWZdLPt2LBzp9UTV2msckQ3OpXTRNv4i4AkzECE/sJzSGQLfubcJ0ky30O4rxmIPIoIYs0n0nLLiEYsS1geWtelia3y7TQhAv~-1~-1~-1; user_session=fuwOxZ7Mkhcte-08UImXWw.6_ozKKUTXSUg1PutRt_ruqt_1tTOVaAYxrSFOyIBzTOTk8z7qXOYnDHjaV1nBPPv4R5Swck2l2JD0I9sWzP2qGXDpqTmpsixZQBDxAox8HzGSVjRElye_VDMugDV5whvQFdtC0H5yvfmR38inrzOfg.1750916970619.86400000.hlnL73fPWCuQA3YHJSpMSIECYVko_OqxfNhkuqHe4YU; bm_s=YAAQJg7EF5e1aaiXAQAALSbJqgM9IkJGWhfqL57/TUWfikadX0vOd/lURZ/kpLiKyJA2UlXB6QWf/4C4l9sCsckkD9rgqZdJnZ/OC4EIYFPjZa2vtZOdms9ZvBTmE/ZaKsqXgPqYs/JwJ+wqpXN9AGauJmaa8nES5PbfvnXR6G2Hep1aNjitmQHMV05tMkPN3eiNqSF/uPlXN+zO+wVVxvopFmFF3iShXIyNJUcEZG6yAPQK8D1HHl/AHOs0hXcNVUI8G1YOpW0JZaG27K5QsX045UXnGzFi/CPb/OeWwNmtAoFdz1RfLh7WsLWslZFj4oLr0zcXqllPvXnulecr57HY9gnjWkYNHvuG5KY4Os6R70GhYTlaqDwa6+FdprIZ/EwlXbJ53ptAlGzoXR1H5Zat0YJT8Uo0S30fF4E6y2v1r3kGhpIlAaaBnM2v9haPVGfheRF9S017I558X7doicH4KE14FD30UJMAf+JjmboO0VvIGlQMXm4lO61snnOsjjgOa5M+3vfViCNReuARvCTOIxLhHiHEfb9XHtVzKsBl1TcSGvBqBzVsfLzLCL1+gxmhUz6f; bm_so=7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=; bm_sz=2D91F866169FB502658FB5005B0AD486~YAAQJg7EF5q1aaiXAQAALSbJqhx0iaEYUlOGz990MvdUh2uKUzYU8BpvZHtYtD0i69Why+elCNLo2tYsRTY/gZ3nGMuhHW9eDrrGAtO2uk2IyqGpmKeGXcnVNW+BKAcnE1EpzPUan/9O1zMwmT18KNlXVeYNbLxwQQAyvD8ildu1/Z0d6pw6KW+5Fu+xSRXnTGces4NOlp8Z7wuoTm3V+8Q8UJfoPSzQjXPO7QvHyII3M6Vchd8zoLM/GPfvLTHvCrjbFKOjrvWS1FEQVfLt8QP0gkOJb53I6XkWF68t3nWC5iZ+XhbMGTO+31ekerTemommXt39ljcU5AlQKpvMarKfxktZVuqtibwzEEq2uzBlqaursXYQ7h2wcStfIhxwpNKYqDLEfFlb0Hzv5MFJbuP02fUJE/Z1nENg~3359029~4403778; utm_track_v1=%7B%22utm_source%22%3A%22direct%22%2C%22utm_medium%22%3A%22direct%22%2C%22trackstart%22%3A1750916999%2C%22trackend%22%3A1750917059%7D; _scid_r=Om_xw-o4sNvz8oBHIRvyHDP0vUKcI5N77AMPaQ; bm_lso=7318A3380DE3D5783E3A4558CABA26221CBF39B5A8C5ECF11887BF95A2186A27~YAAQJg7EF5i1aaiXAQAALSbJqgRyj3dNhCVM17z9licZHGfNd03s7enIBRErEUY5owRNWelIJrsLJ+Lcu2XO7yb7NRnqg7lEQ5KHlJ0QAcrDDodtWbher0Ca3jGUjGyFZL4lB3i93pn7rX9b4r2TjHnS5PDzAdgZbyci63sFxLTS2WLITKrstkCQrpX8mzKNNVxVXUDmxmNsnZHmbKQvnJ9olWFKe/h4kbxdNUx7B0BTFOEikcYw6kCsYbGStwVJYutE486bemb3XlYG3JHGQAKFbllqLka6suGylgWzrIn2NZuiGQXKWfDGBDnik+KxuH00K3nTnbPo05dWI/ugR7luQuhoX13yzyIrQvI0kubGdTNis+E2GQFnwVwJF4qHjCC7nzyr1jRQNYOhYMDsfmDeC1wSDAtmvS/u84Ane/b7WYR96/HWPLaoQFneO43m5r5BCG19k3QEfwVAqjw=^1750917001091; utrid=XW9%2FFVdicUJTam4bakVAMCMxNDg4ODc0NzIxJDI%3D.8f11f6137cc51ca0102c67c069ce4fee; bm_sv=095E1B91BE958E52491C0A14B9FFB242~YAAQJg7EFyy3aaiXAQAAtjrJqhwZcYkLk7WwVx8sAbk8+DzjneCIGnBlNpUBYBD1B0Qe+gU5cGHJPLUu72PY/9SRG6GyIzouCibzkCyFNlMTEFIznMUescbYwpM/k4YWX+KvI+ro9sJorWpFaNymtPx0HBxRmPrqFdLfH5Qt6ozOUapjZYQ7KLdY4+CVCjIOcCBzb+c1FWEd0UNWOhSfDgiRQxxIJxQmQD7DH5vZ7IVPVZ8CVYch0FXMrWOpM02AaA==~1; ak_RT="z=1&dm=myntra.com&si=c3903ef9-b23d-431c-a0b4-2c150e2270c5&ss=mccyr7x4&sl=3&tt=1q6&obo=2&rl=1&ld=11uu&r=48oj4cny&ul=11uw"',
    }
    keyword_name = "tshirts"
    keyword_url = f'https://www.myntra.com/{keyword_name}'
    get_links(cookies, headers, keyword_name, keyword_url)
