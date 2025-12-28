import json
import os
import re
from datetime import datetime
from googletrans import Translator
import requests
import mysql.connector
import scrapy
from deep_translator import GoogleTranslator
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from scrapy.cmdline import execute
import deliveroo.df_config as db
from scrapy.http import HtmlResponse
from deliveroo.items import DeliverooItem


# Todo: Get Delivery Time Field
def deliver_time(request_location_Latitude, request_location_Longitude, drn, vendor_id):
    current_date = datetime.now()
    formatted_date = current_date.strftime("%Y-%m-%d")
    url = "https://api.hk.deliveroo.com/consumer/basket/graphql"

    payload = json.dumps({
        "query": "\n  query getBasketPage($options: BasketOptionsInput!, $capabilities: CapabilitiesInput) {\n    get_basket_page(options: $options, capabilities: $capabilities) {\n      ...basketFields\n    }\n  }\n\n  \n  \n  fragment basketFields on BasketPage {\n    meta {\n      basket {\n        items {\n          ...itemsFields\n        }\n        itemBackupStrategyLabels: item_backup_strategy_labels {\n          id\n          label\n        }\n        subtotalBeforeDiscounts: subtotal_before_discounts {\n          ...moneyFields\n        }\n        subtotalFormatted: subtotal_formatted\n      }\n      summary: basket_page_summary {\n        subtotal: summary_text\n        url: target_url\n      }\n      fullPageUpsell: full_page_upsell {\n        presentation {\n          title\n          allergensSubtitle: allergens_subtitle\n        }\n        menuItems: menu_items {\n          id\n          name\n          is_sponsored_product\n          discount_price: discounted_price {\n            formatted\n            fractional\n          }\n        }\n      }\n      requestUUID: request_uuid\n      isGroupOrder: is_group_order\n      offerMeta: offer_meta {\n        ...offerMetaFields\n      }\n    }\n    fulfillment: meta_fulfillment_time_methods {\n      fulfillment_method_label: label\n      fulfillment_method: method\n      asap {\n        minuteRange: minute_range\n        option_display_label: display_label\n        selected_display_label\n        selected_time {\n          time\n          day\n        }\n        timestamp\n      }\n      days {\n        day\n        day_label\n        times {\n          option_display_label: display_label\n          selected_display_label\n          selected_time {\n            time\n            day\n          }\n          timestamp\n        }\n      }\n    }\n    header: ui_header {\n      title\n      subtitle\n      actions {\n        ...uiActionFields\n      }\n    }\n    sections: ui_sections {\n      ...uiComponentSectionFields\n    }\n    footer: ui_footer {\n      sections: ui_sections {\n        ...uiComponentSectionFields\n      }\n    }\n    modalsOnLoad: modals_on_load {\n      ...uiModalFields\n    }\n    modalDefinitions: modal_definitions {\n      ...uiModalFields\n    }\n    metaTimers: meta_timers {\n      ...timerFields\n    }\n  }\n\n  \n  fragment uiModalFields on UIModal {\n    id\n    trackingId: tracking_id\n    presentationStyle: presentation_style\n    header {\n      title\n      actions {\n        ...uiActionFields\n      }\n    }\n    sections {\n      ...uiComponentSectionFields\n    }\n    footer {\n      sections {\n        ...uiComponentSectionFields\n      }\n    }\n  }\n\n  \n  \n  fragment baseUiSpanFields on UISpan {\n    typeName: __typename\n    ... on UISpanText {\n      key\n      text\n      size\n      trackingId: tracking_id\n      target {\n        ...uiTargetFields\n      }\n      color {\n        ...colorFields\n      }\n      isBold: is_bold\n    }\n    ... on UISpanSpacer {\n      key\n      width\n    }\n    ... on UISpanIcon {\n      key\n      icon: span_icon {\n        name\n        size\n        color {\n          ...colorFields\n        }\n      }\n    }\n    ... on UISpanPlusLogo {\n      key\n      plusLogoSize: size\n      plusLogoColor: color {\n        ...colorFields\n      }\n    }\n    ... on UISpanCountdown {\n      key\n      endsAt: ends_at\n      size\n      color {\n        ...colorFields\n      }\n      isBold: is_bold\n    }\n  }\n\n  fragment uiSpanFields on UISpan {\n    ...baseUiSpanFields\n    ... on UISpanText {\n      isStrikethrough: is_strikethrough\n    }\n    ... on UISpanTag {\n      key\n      typeName: __typename\n      backgroundColor: background_color {\n        ...colorFields\n      }\n      target {\n        ...baseUiTargetFields\n        ... on UITargetModalAction {\n          ...uiTargetModalAction\n        }\n      }\n      uiSpans: ui_spans {\n        ... on UISpanText {\n          typeName: __typename\n          key\n          text\n          size\n          trackingId: tracking_id\n          color {\n            ...colorFields\n          }\n          isBold: is_bold\n        }\n        ... on UISpanSpacer {\n          typeName: __typename\n          key\n          width\n        }\n        ... on UISpanIcon {\n          key\n          icon: span_icon {\n            name\n            size\n            color {\n              ...colorFields\n            }\n          }\n        }\n      }\n    }\n  }\n\n  \n  \n  fragment baseUiTargetFields on UITarget {\n    typeName: __typename\n    ... on UITargetAction {\n      params {\n        id\n        value\n      }\n      action\n      layoutId: layout_id\n    }\n    ... on UITargetMenuItem {\n      menuItemId: menu_item_id\n    }\n    ... on UITargetWebPage {\n      url\n      newWindow: new_window\n      trackingId: tracking_id\n    }\n    ... on UITargetLayoutGroup {\n      layoutGroupId: layout_group_id\n    }\n    ... on UITargetMutation {\n      params {\n        id\n        value\n      }\n      displayName: display_name\n      mutation\n    }\n    ... on UITargetParams {\n      title\n      params {\n        id\n        value\n      }\n      queryParams: query_params\n      trackingId: tracking_id\n    }\n  }\n\n  fragment uiTargetFields on UITarget {\n    ...baseUiTargetFields\n    ... on UITargetGoToCheckout {\n      __typename\n    }\n    ... on UITargetShowEditItemModal {\n      basketItemLegacyId: basket_item_legacy_id\n    }\n    ... on UITargetModalAction {\n      ...uiTargetModalAction\n    }\n    ... on UITargetAddBasketItem {\n      ...uiTargetAddBasketItem\n    }\n    ... on UITargetSetScheduledDeliveryTime {\n      ...uiTargetSetScheduledDeliveryTime\n    }\n    ... on UITargetDismissModal {\n      ...uITargetDismissModalFields\n    }\n    ... on UITargetShowModal {\n      ...uiTargetShowModalFields\n    }\n    ... on UITargetGoBack {\n      ...uiTargetGoBack\n    }\n    ... on UITargetGoToBasket {\n      ...uiTargetGoToBasket\n    }\n    ... on UITargetGoToRestaurants {\n      ...uiTargetGoToRestaurants\n    }\n    ... on UITargetSetRadioButtonValue {\n      value\n    }\n    ... on UITargetToggle {\n      ...uiTargetToggleFields\n    }\n    ... on UITargetUpdateCharityDonationOption {\n      money: value {\n        ...moneyFields\n      }\n    }\n  }\n\n  \n  fragment uiTargetModalAction on UITargetModalAction {\n    trackingId: tracking_id\n    action\n    params {\n      id\n      value\n    }\n    layoutId: layout_id\n  }\n\n  \n  fragment uiTargetAddBasketItem on UITargetAddBasketItem {\n    options {\n      branchId: branch_id\n      fulfillmentMethod: fulfillment_method\n      forceNew: force_new\n      confirmUserAgeOver18: confirm_user_age_over_18\n      location {\n        lat\n        lon\n      }\n    }\n    item {\n      menuItemDrnId: menu_item_drn_id\n      quantity\n      modifierItems: modifier_items {\n        ...addModifierItemFields\n      }\n    }\n  }\n\n  \n  fragment addModifierItemFields on AddModifierItemOptions {\n    menuItemLegacyId: menu_item_legacy_id\n    parentMenuItemId: parent_menu_item_id\n    quantity\n    modifierGroupId: modifier_group_id\n  }\n\n  \n  fragment uITargetDismissModalFields on UITargetDismissModal {\n    modalId: modal_id\n  }\n\n  \n  fragment uiTargetSetScheduledDeliveryTime on UITargetSetScheduledDeliveryTime {\n    timestamp\n  }\n\n  \n  fragment uiTargetShowModalFields on UITargetShowModal {\n    modalId: modal_id\n  }\n\n  \n  fragment uiTargetToggleFields on UITargetToggle {\n    id\n    nextStatus: next_status\n  }\n\n  \n  fragment uiTargetGoBack on UITargetGoBack {\n    url\n  }\n\n  \n  fragment uiTargetGoToBasket on UITargetGoToBasket {\n    options {\n      fulfillmentMethod: fulfillment_method\n    }\n  }\n\n  \n  fragment uiTargetGoToRestaurants on UITargetGoToRestaurants {\n    url\n  }\n\n  \n  \n  fragment uiBasicComponentFields on UIBasicRowComponent {\n    typeName: __typename\n    ... on UIBasicRowTextContent {\n      key\n      textContent: content {\n        ...uiLineFields\n      }\n    }\n    ... on UIBasicRowImageContent {\n      key\n      imageContent: content {\n        ... on Icon {\n          name\n        }\n      }\n    }\n  }\n\n  \n  fragment baseUiListComponentFields on UIListComponent {\n    typeName: __typename\n  }\n\n  fragment uiListComponentFields on UIListComponent {\n    ...baseUiListComponentFields\n    ... on UIButton {\n      ...uiButtonFields\n    }\n    ... on UIButtonGroup {\n      ...uiButtonGroup\n    }\n    ... on UIBasicRow {\n      ...uiBasicRow\n    }\n    ... on UIBenefitsBreakdown {\n      ...uiBenefitsBreakdown\n    }\n    ... on UIBanner {\n      ...uiBanner\n    }\n    ... on UICarousel {\n      ...uiCarouselFields\n    }\n    ... on UITextAreaInput {\n      ...uiTextAreaInputFields\n    }\n    ... on UICharityDonation {\n      ...uiCharityDonationFields\n    }\n    ... on UILargeBanner {\n      ...uiLargeBanner\n    }\n    ... on UICharityDonationOptions {\n      ...uiCharityDonationOptionsFields\n    }\n  }\n\n  \n  fragment uiButtonGroup on UIButtonGroup {\n    key\n    buttons {\n      ...uiButtonFields\n    }\n  }\n\n  \n  fragment uiLargeBanner on UILargeBanner {\n    key\n    mainBackgroundColor: main_background_color {\n      ...baseUiBackgroundColor\n    }\n    contents {\n      ...uiLineFields\n    }\n    icon {\n      ...uiLargeBannerIcon\n    }\n    detailsBackgroundColor: details_background_color {\n      ...baseUiBackgroundColor\n    }\n    details {\n      ...uiBasicRow\n    }\n  }\n\n  \n  fragment uiLargeBannerIcon on UILargeBannerIcon {\n    typeName: __typename\n    ... on Icon {\n      ...iconFields\n    }\n    ... on StaticImage {\n      ...uiBaseStaticAsset\n    }\n    ... on Illustration {\n      illustrationName: name\n    }\n    ... on UIRewardsProgress {\n      ...uiRewardsProgress\n    }\n  }\n\n  \n  fragment uiRewardsProgress on UIRewardsProgress {\n    key\n    steps\n    completed\n    trackingId: tracking_id\n  }\n\n  \n  fragment uiButtonFields on UIButton {\n    typeName: __typename\n    key\n    trackingId: tracking_id\n    text\n    type\n    lines: ui_line {\n      ...uiLineFields\n    }\n    target {\n      ...uiTargetFields\n    }\n    isDestructive: is_destructive\n  }\n\n  \n  fragment uiCarouselFields on UICarousel {\n    key\n    trackingId: tracking_id\n    carouselHeader: header\n    subheader\n    components {\n      ...uiCarouselComponentFields\n    }\n    stretchContent: stretch_content\n    action: ui_action {\n      ...uiActionFields\n    }\n  }\n\n  \n  fragment uiTextAreaInputFields on UITextAreaInput {\n    key\n    placeholder\n    maxLength: max_length\n    initialValue: initial_value\n    helpMessage: help_message\n  }\n\n  \n  fragment uiStaticAsset on UIStaticAsset {\n    ...uiBaseStaticAsset\n    ... on Icon {\n      backgroundColor: background_color {\n        ...colorFields\n      }\n    }\n  }\n\n  \n  fragment uiBaseStaticAsset on UIStaticAsset {\n    typeName: __typename\n    ... on Icon {\n      name\n      size\n      color {\n        ...colorFields\n      }\n    }\n    ... on StaticImage {\n      imageName: name\n      imageSize: size\n    }\n  }\n\n  \n  \n  fragment baseUiComponentSectionFields on UIComponentSection {\n    typeName: __typename\n    ... on UIListSection {\n      key\n      sectionId: section_id\n      trackingId: tracking_id\n      header\n      subheader\n      maxColumns: max_columns\n      components {\n        ...uiListComponentFields\n      }\n      action: ui_action {\n        ...uiActionFields\n      }\n    }\n    ... on UIGridSection {\n      key\n      sectionId: section_id\n      trackingId: tracking_id\n      header\n      subheader\n      components {\n        ...uiGridComponentFields\n      }\n    }\n    ... on UICarouselSection {\n      key\n      sectionId: section_id\n      trackingId: tracking_id\n      header\n      subheader\n      components {\n        ...uiCarouselComponentFields\n      }\n      stretchContent: stretch_content\n      action: ui_action {\n        ...uiActionFields\n      }\n    }\n  }\n\n  fragment uiComponentSectionFields on UIComponentSection {\n    ...baseUiComponentSectionFields\n    ... on UIListSection {\n      style\n      uiLines: ui_lines {\n        ...uiLineFields\n      }\n    }\n  }\n\n  \n  \n  fragment baseUiGridComponentFields on UIGridComponent {\n    typeName: __typename\n  }\n\n  fragment uiGridComponentFields on UIGridComponent {\n    ...baseUiGridComponentFields\n  }\n\n  \n  \n  fragment baseUiCarouselComponentFields on UICarouselComponent {\n    typeName: __typename\n  }\n\n  fragment uiCarouselComponentFields on UICarouselComponent {\n    ...baseUiCarouselComponentFields\n    ... on UIRecommendedItemCard {\n      key\n      description {\n        ...uiLineFields\n      }\n      image {\n        ...imageFields\n      }\n      quickAddTarget: quickadd_target {\n        ...baseUiTargetFields\n        ... on UITargetAddBasketItem {\n          ...uiTargetAddBasketItem\n        }\n      }\n      coreTarget: target {\n        ...baseUiTargetFields\n        ... on UITargetAddBasketItem {\n          ...uiTargetAddBasketItem\n        }\n      }\n      trackingId: tracking_id\n      trackingProperties: tracking_properties\n    }\n  }\n\n  \n  fragment uiComponentFields on UIBasicRowComponent {\n    ...uiBasicComponentFields\n    ... on UIBasicRowImageContent {\n      ...uiBasicRowImageContent\n    }\n    ... on UIRiderTipStepper {\n      ...uiRiderTipStepper\n    }\n    ... on UIRadioButtonBasicRowComponent {\n      ...uiRadioButtonBasicRowComponent\n    }\n    ... on UIBasicRowToggle {\n      ...uiBasicRowToggle\n    }\n  }\n\n  \n  fragment uiLineFields on UILine {\n    typeName: __typename\n    ... on UITextLine {\n      key\n      align\n      spans: ui_spans {\n        ...uiSpanFields\n      }\n      maxLines: max_lines\n    }\n    ... on UITitleLine {\n      key\n      text\n      color {\n        ...colorFields\n      }\n      size\n    }\n  }\n\n  \n  fragment uiActionFields on UIAction {\n    key\n    icon {\n      ...iconFields\n    }\n    lines: ui_lines {\n      ...uiLineFields\n    }\n    target {\n      ...uiTargetFields\n    }\n    targetPresentational: target_presentational {\n      ...uiLineFields\n    }\n    trackingId: tracking_id\n    contentDescription: content_description\n  }\n\n  \n  fragment iconFields on Icon {\n    name\n    size\n    color {\n      ...colorFields\n    }\n  }\n\n  \n  fragment colorFields on Color {\n    red\n    green\n    blue\n    hex\n    name\n    alpha\n  }\n\n  \n  fragment uiBasicRow on UIBasicRow {\n    rowType: type\n    contentStart: content_start {\n      ...uiComponentFields\n    }\n    contentMain: content_main {\n      ...uiComponentFields\n    }\n    contentEnd: content_end {\n      ...uiComponentFields\n    }\n    target {\n      ...uiTargetFields\n    }\n    key\n    trackingId: tracking_id\n  }\n\n  \n  fragment uiBasicRowImageContent on UIBasicRowImageContent {\n    key\n    imageContent: content {\n      ...uiStaticAsset\n    }\n  }\n\n  \n  fragment baseUiBackgroundColor on UIBackgroundColor {\n    typeName: __typename\n    ... on Color {\n      ...colorFields\n    }\n    ... on ColorGradient {\n      from {\n        ...colorFields\n      }\n      to {\n        ...colorFields\n      }\n    }\n  }\n\n  \n  fragment uiBenefitsBreakdownHeader on UIBenefitsBreakdownHeader {\n    background {\n      ...baseUiBackgroundColor\n    }\n    uiLines: ui_lines {\n      ...uiLineFields\n    }\n    contentDescription: content_description\n  }\n\n  \n  fragment uiBenefitsBreakdown on UIBenefitsBreakdown {\n    key\n    header {\n      ...uiBenefitsBreakdownHeader\n    }\n    content {\n      ...uiBasicRow\n    }\n    contentBackground: content_background {\n      ...baseUiBackgroundColor\n    }\n    pointerPosition: pointer_position\n  }\n\n  \n  fragment uiBanner on UIBanner {\n    key\n    background {\n      ...baseUiBackgroundColor\n    }\n    bannerContent: content {\n      ...uiBasicRow\n    }\n  }\n\n  \n  fragment uiCharityDonationFields on UICharityDonation {\n    key\n    title\n    subtitle\n    charityImage: image {\n      ...imageFields\n    }\n  }\n\n  \n  fragment itemsFields on BasketItem {\n    legacyId: legacy_id\n    menuItemLegacyId: menu_item_legacy_id\n    menuItemDrnId: menu_item_drn_id\n    name\n    description\n    quantity\n    totalPriceFormatted: total_price_formatted\n    discountedTotalPriceFormatted: discounted_total_price_formatted\n    modifierItems: modifier_items {\n      ...modifierItemFields\n    }\n    backupStrategy: backup_strategy\n    availableBackupStrategies: available_backup_strategies\n  }\n\n  \n  fragment modifierItemFields on ModifierBasketItem {\n    legacyId: legacy_id\n    menuItemLegacyId: menu_item_legacy_id\n    menuItemDrnId: menu_item_drn_id\n    modifierId: modifier_id\n    parentModifierItemId: parent_modifier_item_id\n    parentMenuItemLegacyId: parent_menu_item_legacy_id\n    parentMenuItemDrnId: parent_menu_item_drn_id\n    name\n    description\n    quantity\n    totalPriceFormatted: total_price_formatted\n    discountedTotalPriceFormatted: discounted_total_price_formatted\n    modifierGroupId: modifier_group_id\n    path\n  }\n\n  \n  fragment imageFields on Image {\n    url\n    type\n    altText: alt_text\n  }\n\n  \n  fragment uiRiderTipStepper on UIRiderTipStepper {\n    key\n    decrementIcon: decrement_icon {\n      ...iconFields\n    }\n    incrementIcon: increment_icon {\n      ...iconFields\n    }\n    decrementContentDescription: decrement_content_description\n    incrementContentDescription: increment_content_description\n    stepAmount: step_amount {\n      ...moneyFields\n    }\n    maxAmount: max_amount {\n      ...moneyFields\n    }\n    currentAmount: current_amount {\n      ...moneyFields\n    }\n  }\n\n  \n  fragment uiBasicRowToggle on UIBasicRowToggle {\n    key\n    selected\n  }\n\n  \n  fragment moneyFields on Money {\n    fractional\n    currency\n    currencySymbol: currency_symbol\n    fractionalConversion: fractional_conversion\n    formatted\n  }\n\n  \n  fragment uiRadioButtonBasicRowComponent on UIRadioButtonBasicRowComponent {\n    isSelected: is_selected\n    value\n  }\n\n  \n  fragment timerFields on Timer {\n    endsAt: ends_at\n    target {\n      ...uiTargetFields\n    }\n  }\n\n  \n  fragment offerMetaFields on OfferMeta {\n    progressBar: progress_bar {\n      ...progressBarFields\n    }\n  }\n\n  \n  fragment progressBarStateFields on OfferProgressBarState {\n    line {\n      ...uiLineFields\n    }\n    timer {\n      ...uiLineFields\n    }\n    progressBarColor: progress_bar_color {\n      ...colorFields\n    }\n  }\n\n  \n  fragment progressBarFields on OfferProgressBar {\n    offer {\n      minimumOrderValue: minimum_order_value {\n        ...currencyFields\n      }\n    }\n    display\n    initial {\n      ...progressBarStateFields\n    }\n    inProgress: in_progress {\n      ...progressBarStateFields\n    }\n    complete {\n      ...progressBarStateFields\n    }\n  }\n\n  \n  fragment currencyFields on Currency {\n    code\n    fractional\n    formatted\n    presentational\n  }\n\n  \n  fragment uiCharityDonationOptionsFields on UICharityDonationOptions {\n    key\n    trackingId: tracking_id\n    label\n    options {\n      selected\n      label\n      target {\n        ...uiTargetFields\n      }\n      trackingId: tracking_id\n    }\n  }\n\n\n",
        "variables": {
            "options": {
                "fulfillment_method": "DELIVERY",
                "delivery_time": {
                    "time": "ASAP",
                    "day": "TODAY"
                },
                "location": {
                    "lat": request_location_Latitude,
                    "lon": request_location_Longitude
                },
                "branch_id": drn
            },
            "capabilities": {
                "ui_list_components": [
                    "UI_BUTTON_GROUP",
                    "UI_CHARITY_DONATION_OPTIONS"
                ],
                "ui_action_types": [
                    "CHANGE_ADDRESS",
                    "GO_TO_PLUS_SIGN_UP",
                    "REFRESH_BASKET"
                ]
            }
        }
    })
    headers = {
        'accept': 'application/json, application/vnd.api+json',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en',
        'content-type': 'application/json',
        'origin': 'https://deliveroo.hk',
        'priority': 'u=1, i',
        'referer': 'https://deliveroo.hk/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'x-roo-client': 'consumer-web-app',
        'x-roo-external-device-id': 'a2311f6a-7924-48c7-affa-b1349f4d8ee4',
        'x-roo-guid': '8138c8de-c351-45a8-b7cf-39c6d877b3e8',
        'x-roo-session-guid': 'f2b91832-0d23-4325-bc76-fbe5e2d8f582',
        'x-roo-sticky-guid': '8138c8de-c351-45a8-b7cf-39c6d877b3e8',
        'Cookie': '__cf_bm=FjqOgdYV1GAweukWG34kOY54meVMOk6cgiTnX1WeyZs-1725269005-1.0.1.1-4tZkLhXz82iPIUAHEYBiFq2W46BPcTaQEhFmyieHgnmlLcR.EWARKhdSDxJB9hXi4Pdr097luUY5G5pk_sct_wHVhYVwC13bTRFkhYT1bkw; _cfuvid=m5mvZKub0jX9HgTeOKnRS9sZzNGvG24ZnapMC26NgsI-1725266087842-0.0.1.1-604800000'
    }

    # Todo: requests for delivery_time filed
    delivery_response = requests.request("POST", url, headers=headers, data=payload)
    if delivery_response.status_code != 200:
        for k in range(3):
            delivery_response = requests.request("POST", url, headers=headers, data=payload)
            if delivery_response.status_code == 200:
                break
    # path = f"C:\\Actowiz\\pagesave\\Deliveroo\\{formatted_date}\\Cart\\"
    path = db.pagesave_cart_path
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = path + vendor_id + ".html"
    file_name = file_name.replace("\\", '\\\\')
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(delivery_response.text)
    deliver_json = json.loads(delivery_response.text)
    try:
        delivery_time = deliver_json['data']['get_basket_page']['fulfillment'][0]['asap']['minuteRange']
    except:
        delivery_time = ""
    return delivery_time


class DataSpider(scrapy.Spider):
    name = "data"
    start_urls = ["https://example.com"]

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def parse(self, response, **kwargs):
        current_date = datetime.now()
        formatted_date = current_date.strftime("%Y_%m_%d")
        mydb = mysql.connector.connect(
            host=db.host,
            user=db.username,
            password=db.password,
            database=db.database_name
        )

        mycursor = mydb.cursor()
        mycursor.execute(f"select * from {db.restaurant_links} where status = 'pending'  limit {self.a},{self.b};")
        myresult = mycursor.fetchall()
        for d in myresult:
            url = d[4]
            vendor_id = d[2]
            print(vendor_id, "+++++++++|||||||||===", url)
            lead_source = "Deliveroo"
            type = "vendor"
            scraped_url = url
            restaurant_url = url
            phone_number = ""
            opening_hours = ""
            minimum_order_price = ""
            free_delivery_option = "1"
            delivery_fee = ""
            distance = ""
            distance_unit = ""
            promotion_tags_delivery = ""
            promotion_tags_pickup = ""
            is_open = "True"

            payload = {}
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
                'cache-control': 'max-age=0',
                'cookie': 'roo_guid=8138c8de-c351-45a8-b7cf-39c6d877b3e8; roo_guid=8138c8de-c351-45a8-b7cf-39c6d877b3e8; shield_FPC=SCfQ8I7q6gH6gM1LWepuUTvRu1gvnqfWv5; _pxvid=9a8a8160-66a0-11ef-9c06-8676d3121305; __pxvid=9aceaffc-66a0-11ef-aa68-0242ac120002; _gcl_au=1.1.1423357780.1725002548; _ga=GA1.1.750316016.1725002545; _scid=3abfdd1a-aef0-4a89-921e-eb4f595bd4da; _tt_enable_cookie=1; _ttp=JmQ5r8-_Sv04Uyd3hwHjXTlMvkt; _pin_unauth=dWlkPU5XUmhaakkzWkRrdE1qazJZaTAwWmpOaExUaGpabVF0T1dWaFltRmpOV1ZoWWpBMg; _ScCbts=%5B%5D; _fbp=fb.1.1725002549903.819407487304369002; _sctr=1%7C1724956200000; external_device_id=a2311f6a-7924-48c7-affa-b1349f4d8ee4; cwa_user_preferences={%22deviceStats%22:{%22innerWidth%22:1280}%2C%22seen_modals%22:{%22nc_promos_nux_2814ac7a-87db-4e08-858d-68f91c982634%22:{%22id%22:%22nc_promos_nux_2814ac7a-87db-4e08-858d-68f91c982634%22%2C%22timestamp%22:1725002571}%2C%22flash_deals%22:{%22id%22:%22flash_deals%22%2C%22timestamp%22:1725002730}}}; cf_clearance=ToRe_MsDNTn1RSX0iYIDhyCwSOVe6L7Mgzw4zHHyylk-1725003269-1.2.1.1-0X4dKIQdLYTqXbJiPoJroNL1FzyPSlPp8cK5pLm3KHtJakr_SDAtPNE_F2sP6Fi.GClqlG2WtwYwU2oqWK1Ob1hVntDsiCczfA0FuQQ4AvW_oN5HG4S2a79JXOcgUDslZ6q4E6u1z9I4cvOLz.vGGFsUywJqnijfMx2cNz3PYHwLi.ytGzmLr644U1va7ivmf7Adjh8SCDaPuU1CIE22ZNI_47tUrF3ZT0Nla0Fo4F900vEM9rQTozkcwm4.JzvzLWNOYOwwKbTJMDJO8j9g_TtwK3j2cI3S17kbXOLue6WemWnqi8EreJjSjoliHMTksdpfl5mtH.YNIY5Jffwn90Mnvl3kKyDRq_sH101o0bDZiNLiSweZszQuuFz.1FJRfpRtlpkc823BcgtimKzcANVuRQPmtFtcZEeyDtC6h3k; location_data=eyJsb2NhdGlvbiI6eyJjb29yZGluYXRlcyI6WzExNC4xNTkyNTk2LDIyLjI4NTIzMl0sImlkIjpudWxsLCJmb3JtYXR0ZWRfYWRkcmVzcyI6IlR3byBJbnRlcm5hdGlvbmFsIEZpbmFuY2UgQ2VudHJlLCA4IEZpbmFuY2UgU3QsIENlbnRyYWwsIEhvbmcgS29uZyIsInBsYWNlX2lkIjoiQ2hJSjYxaFpyR01BQkRRUlFxWWgzWXRadFA0IiwicGluX3JlZmluZWQiOmZhbHNlLCJjaXR5IjpudWxsfX0.; roo_session_guid=f2b91832-0d23-4325-bc76-fbe5e2d8f582; locale=eyJsb2NhbGUiOiJlbiJ9; __cf_bm=SsgERUaRt3fMkpgqZI8PP5uFaPsm3QkBwkzPUkuflsE-1725255152-1.0.1.1-0ihk4sXhsbroG.rD03vsqHdUgp4myESUJj3RYNQPatLcPT18ynAwu9MLoryHu6VqIZ0Dj5bOozA.mygjeVCpTrjHcz1p7sq6CL_DoSSZC3c; roo_super_properties=eyJjb250ZXh0Ijp7InVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMjguMC4wLjAgU2FmYXJpLzUzNy4zNiIsImlwIjoiNS42Mi41Ni4yNTEiLCJsb2NhdGlvbiI6eyJjb3VudHJ5IjoiSG9uZyBLb25nIn0sImxvY2FsZSI6ImVuIn0sIlJlcXVlc3RlZCBMb2NhbGUiOiJlbiIsIlJvb0Jyb3dzZXIiOiJDaHJvbWUiLCJSb29Ccm93c2VyVmVyc2lvbiI6IjEyOCIsIkRldmljZSBUeXBlIjoiZGVza3RvcCIsIlRMRCI6ImhrIiwiUGxhdGZvcm0iOiJ3ZWIiLCJMb2NhbGUiOiJlbiIsIndoaXRlX2xhYmVsX2JyYW5kIjoiY29yZSJ9; pxcts=c43ac8d4-68ec-11ef-8308-f8eb2aa81e42; _clck=1dcfr8c%7C2%7Cfou%7C0%7C1703; OptanonAlertBoxClosed=2024-09-02T05:36:46.240Z; _ga_ZW8Q7SZ57X=GS1.1.1725255155.5.1.1725255409.54.0.0; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+02+2024+11%3A06%3A49+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=dd291773-4cd7-41da-8bfb-acfb3ffe8a34&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=H95%3A1%2CH5%3A1%2CH111%3A1%2CH79%3A1%2CH80%3A1%2CH86%3A1%2CH85%3A1%2CH4%3A1%2CH155%3A1%2CH74%3A1%2CH38%3A1%2CH89%3A1%2CH99%3A1%2CH108%3A1%2CH167%3A1%2CH20%3A1%2CH77%3A1%2CH164%3A1%2CH156%3A1%2CH101%3A1%2CH104%3A1%2CH25%3A1%2CH162%3A1%2CH83%3A1%2CH39%3A1%2CH159%3A1&genVendors=&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false; _scid_r=3abfdd1a-aef0-4a89-921e-eb4f595bd4da; _uetsid=c51c056068ec11efb96a498dddceabbc; _uetvid=9d34e33066a011efae244b85347c60fb; _clsk=wbhc16%7C1725255415317%7C2%7C0%7Cn.clarity.ms%2Fcollect; external_device_id=a2311f6a-7924-48c7-affa-b1349f4d8ee4; locale=eyJsb2NhbGUiOiJlbiJ9; roo_guid=8138c8de-c351-45a8-b7cf-39c6d877b3e8',
                'priority': 'u=0, i',
                'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                'sec-ch-ua-arch': '"x86"',
                'sec-ch-ua-bitness': '"64"',
                'sec-ch-ua-full-version': '"128.0.6613.113"',
                'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.113", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.113"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"10.0.0"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            # Todo: Second Requests
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                response = HtmlResponse(body=response.text, url=url, encoding='utf-8')
                current_date = datetime.now()
                formatted_date_pagesave = current_date.strftime("%Y-%m-%d")
                # path = f"C:\\Actowiz\\pagesave\\Deliveroo\\{formatted_date_pagesave}\\Data\\"
                path = db.pagesave_data_path
                if not os.path.exists(path):
                    os.makedirs(path)
                file_name = path + vendor_id + ".html"
                file_name = file_name.replace("\\", '\\\\')
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(response.text)

                data_json = response.xpath('//script[@type="application/json"]//text()').get()
                json_data = json.loads(data_json)
                try:
                    rest_name = json_data['props']['initialState']['menuPage']['menu']['meta']['restaurant']['name']
                except:
                    rest_name = ""

                if rest_name:
                    if "(" in rest_name and ")" in rest_name:
                        match = re.search(r'\((.*?)\)', rest_name)
                        try:
                            extracted_value = match.group(1)
                        except:
                            extracted_value = ""
                        updated_string = re.sub(r'\(.*?\)', '', rest_name).strip()
                        branch_name_local = extracted_value
                        branch_name = GoogleTranslator(source='auto', target="en").translate(extracted_value)
                        name_local = updated_string
                        name = GoogleTranslator(source='auto', target="en").translate(updated_string)
                    else:
                        translated_text = GoogleTranslator(source='auto', target="en").translate(rest_name)
                        name = translated_text
                        name_local = rest_name
                        branch_name = ""
                        branch_name_local = ""
                    other_cats = []
                    category = ""
                    other_cat = json_data['props']['initialState']['menuPage']['menu']['layoutGroups']
                    for o in other_cat:
                        try:
                            # props.initialState.menuPage.menu.layoutGroups[0].layouts[2].header
                            other_c = o['layouts']
                            try:
                                for oo in other_c:
                                    try:
                                        hearder = oo['header']
                                        if hearder == "Browse by category":
                                            other_cc = oo['blocks']
                                            for ot in other_cc:
                                                lines = ot['lines']
                                                for s in lines:
                                                    span = s['spans']
                                                    for t in span:
                                                        cat_t = t['text']
                                                        other_cats.append(cat_t)
                                    except Exception as e:
                                        print(e)
                            except Exception as e:
                                print(e)
                        except Exception as e:
                            print(e)
                    if other_cats == []:
                        category_data = json_data['props']['initialState']['menuPage']['menu']['meta']['categories']
                        category_list = []
                        for c in category_data:
                            category_name = c['name'].strip().replace("\\n", "")
                            category_list.append(category_name)
                        phone_details = json_data['props']['initialState']['menuPage']['menu']['layoutGroups']
                        promo = []
                        for p in phone_details:
                            try:
                                p_data = p['layouts']
                                for pd in p_data:
                                    mm_data = pd['header']
                                    if mm_data == "Popular with other people":
                                        category_list.append(mm_data)
                            except Exception as e:
                                print(e)
                        category = " , ".join(category_list)

                    is_delivery_available = "True"
                    is_pickup_enabled = "True"
                    main_data = json_data['props']['initialState']['menuPage']['menu']['header']['headerTags']['lines']
                    cuisin_list = []
                    for m in main_data:
                        middle = m['spans']
                        for f in middle:
                            try:
                                text = f['text']
                                if "km away" in text:
                                    distance = text
                                    distance = distance.replace(" km away", "")
                                    distance_unit = "km"
                                elif "Closes at" in text or "Opens at" in text:
                                    opening_hours = text
                                    if "close" in opening_hours.lower():
                                        is_open = "True"
                                    else:
                                        is_open = "False"
                                elif "minimum" in text:
                                    minimum_order_price = text
                                    minimum_order_price = minimum_order_price.replace("$", "").replace(" minimum", "")
                                elif "delivery" in text:
                                    delivery_charges = text
                                    if "Free" in delivery_charges:
                                        free_delivery_option = "1"
                                        delivery_fee = ""
                                    else:
                                        free_delivery_option = "0"
                                        delivery_fee = delivery_charges.replace("delivery", "")
                                elif text != "·" and "." not in text and "(" not in text:
                                    cuisin_list.append(text)
                            except:
                                text = ""

                    cuisine = " , ".join(cuisin_list)
                    latitude = ""
                    longitude = ""
                    image = json_data['props']['initialState']['menuPage']['menu']['meta']['metatags']['image']
                    others = ""
                    other = dict()
                    pop_list = []
                    other['shop_image'] = image
                    new_data = json_data['props']['initialState']['menuPage']['menu']['layoutGroups']
                    for n in new_data:
                        about_data = n['layouts']
                        for an in about_data:
                            head = an['header']
                            print(head)
                            if head == "Popular with other people":
                                new_c = an['carouselBlocks']
                                for nc in new_c:
                                    pop_dict = {}
                                    # pop_name=nc['image']['altText']
                                    # pop_image=nc['image']['url']
                                    pop_id = nc['id']
                                    item_loop = json_data['props']['initialState']['menuPage']['menu']['meta']['items']
                                    for items in item_loop:
                                        item_id = items['id']
                                        if item_id == pop_id:
                                            pop_price = items['price']['formatted']
                                            pop_dict['name'] = items['name'].replace("'", "''")
                                            pop_dict['price'] = pop_price
                                            try:
                                                pop_dict['image'] = items['image']['url']
                                            except:
                                                pop_dict['image'] = ""
                                    pop_list.append(pop_dict)
                            try:
                                ad = an['blocks']
                                for rr in ad:
                                    rd = rr['lines']
                                    for we in rd:
                                        spa = we['spans']
                                        for sp in spa:
                                            new_text = sp['text']
                                            if "About" in head:
                                                other[head.replace("'", "''")] = new_text.replace("\n", "").replace(
                                                    "\t", "").replace("'", "''").replace('"', "")
                                            if head == "Allergens":
                                                other[head.replace("'", "''")] = new_text.replace("\n", "").replace(
                                                    "\t", "").replace("'", "''").replace('"', "")
                            except Exception as e:
                                print(e)

                    # Todo: Third Requests
                    drn = json_data['props']['initialState']['menuPage']['menu']['meta']['restaurant']['drnId']
                    basket_url_u = "https://api.hk.deliveroo.com/consumer/ugc-service/graphql/"
                    basket_url = f"http://api.scrape.do?token=aa48e53ef4934d95a56acecacaec8fe454ebf634a98&url={basket_url_u}&device=desktop"
                    payload = json.dumps({
                        "variables": {
                            "options": {
                                "partner_drn_id": drn,
                                "pagination": {
                                    "limit": 10000,
                                    "offset": 0
                                },
                                "params": []
                            },
                            "trackingUUID": ""
                        },
                        "query": "\n  query get_partner_reviews($options: SearchOptionsInput!, $trackingUUID: String!) {\n    reviewData: get_partner_reviews(options: $options, tracking_uuid: $trackingUUID) {\n      layouts: ui_review_layouts {\n        typeName: __typename\n        ... on PartnerReviewsLayout {\n          title\n          sortOptions: sort_options {\n            selected\n            target {\n              ...uiTargetFields\n            }\n          }\n          reviews {\n            ...uiPartnerReview\n          }\n        }\n        ... on PartnerRatingBreakdownLayout {\n          title\n          ratingBreakdown: rating_breakdown {\n            averageRating: average_rating\n            color: rating_color {\n              ...colorFields\n            }\n            numberOfStars: number_of_stars\n            totalStars: total_stars\n            reviewCount: review_count\n            ratingBreakdownRows: rating_breakdown_rows {\n              number\n              percent\n              color {\n                ...colorFields\n              }\n            }\n          }\n        }\n        ... on PartnerReviewsButtonLayout {\n          title\n          button {\n            text\n            uiTarget: target {\n              ...uiTargetFields\n            }\n            uiTheme: ui_theme\n          }\n        }\n      }\n      meta {\n        trackingId: tracking_id\n        partnerDrnId: partner_drn_id\n        appliedSort: applied_sort\n      }\n    }\n  }\n\n  \n  fragment colorFields on Color {\n    red\n    green\n    blue\n    hex\n    name\n    alpha\n  }\n\n  \n  fragment uiPartnerReview on PartnerReview {\n    id\n    reviewer {\n      username\n      displayName: display_name\n      avatar {\n        ... on Image {\n          url\n          altText: alt_text\n        }\n      }\n    }\n    tags {\n      text\n      backgroundColor: background_color {\n        ...colorFields\n      }\n      textColor: text_color {\n        ...colorFields\n      }\n      icon {\n        name\n      }\n    }\n    textComment: text_comment\n    starRating: star_rating {\n      totalStars: total_stars\n      appliedStars: applied_stars\n      color {\n        ...colorFields\n      }\n    }\n    date\n    uiTargets: ui_targets {\n      ...uiTargetFields\n    }\n    voteUi: vote_ui {\n      defaultLine: ui_line {\n        ...uiLineFields\n      }\n      state\n      actions {\n        icon {\n          ...iconFields\n        }\n        line: ui_line {\n          ...uiLineFields\n        }\n        state\n        descriptor\n        selectedIconColor: selected_icon_color {\n          ...colorFields\n        }\n        unselectedIconColor: unselected_icon_color {\n          ...colorFields\n        }\n        target {\n          params {\n            id\n            value\n          }\n          displayName: display_name\n          mutation\n        }\n      }\n    }\n  }\n\n  \n  \n  fragment baseUiTargetFields on UITarget {\n    typeName: __typename\n    ... on UITargetAction {\n      params {\n        id\n        value\n      }\n      action\n      layoutId: layout_id\n    }\n    ... on UITargetMenuItem {\n      menuItemId: menu_item_id\n    }\n    ... on UITargetWebPage {\n      url\n      newWindow: new_window\n      trackingId: tracking_id\n    }\n    ... on UITargetLayoutGroup {\n      layoutGroupId: layout_group_id\n    }\n    ... on UITargetMutation {\n      params {\n        id\n        value\n      }\n      displayName: display_name\n      mutation\n    }\n    ... on UITargetParams {\n      title\n      params {\n        id\n        value\n      }\n      queryParams: query_params\n      trackingId: tracking_id\n    }\n  }\n\n  fragment uiTargetFields on UITarget {\n    ...baseUiTargetFields\n    ... on UITargetAction {\n      displayName: display_name\n    }\n  }\n\n  \n  \n  fragment baseUiSpanFields on UISpan {\n    typeName: __typename\n    ... on UISpanText {\n      key\n      text\n      size\n      trackingId: tracking_id\n      target {\n        ...uiTargetFields\n      }\n      color {\n        ...colorFields\n      }\n      isBold: is_bold\n    }\n    ... on UISpanSpacer {\n      key\n      width\n    }\n    ... on UISpanIcon {\n      key\n      icon: span_icon {\n        name\n        size\n        color {\n          ...colorFields\n        }\n      }\n    }\n    ... on UISpanPlusLogo {\n      key\n      plusLogoSize: size\n      plusLogoColor: color {\n        ...colorFields\n      }\n    }\n    ... on UISpanCountdown {\n      key\n      endsAt: ends_at\n      size\n      color {\n        ...colorFields\n      }\n      isBold: is_bold\n    }\n  }\n\n  fragment uiSpanFields on UISpan {\n    ...baseUiSpanFields\n  }\n\n  \n  fragment uiLineFields on UILine {\n    typeName: __typename\n    ... on UITextLine {\n      key\n      align\n      spans: ui_spans {\n        ...uiSpanFields\n      }\n      maxLines: max_lines\n    }\n    ... on UITitleLine {\n      key\n      text\n      color {\n        ...colorFields\n      }\n      size\n    }\n  }\n\n  \n  fragment iconFields on Icon {\n    name\n    size\n    color {\n      ...colorFields\n    }\n  }\n\n"
                    })
                    headers = {
                        'accept': 'application/json, application/vnd.api+json',
                        'accept-encoding': 'gzip, deflate, br, zstd',
                        'accept-language': 'en',
                        'content-type': 'application/json',
                        'origin': 'https://deliveroo.hk',
                        'priority': 'u=1, i',
                        'referer': 'https://deliveroo.hk/',
                        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'cross-site',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                        'x-roo-client': 'consumer-web-app',
                        'x-roo-external-device-id': 'a2311f6a-7924-48c7-affa-b1349f4d8ee4',
                        'x-roo-guid': '8138c8de-c351-45a8-b7cf-39c6d877b3e8',
                        'x-roo-session-guid': 'f2b91832-0d23-4325-bc76-fbe5e2d8f582',
                        'x-roo-sticky-guid': '8138c8de-c351-45a8-b7cf-39c6d877b3e8',
                        # 'Cookie': '__cf_bm=4wampG_N6VjaUIJYJSP3V.TXNL8pmsTKLjXcFieFCEo-1725266087-1.0.1.1-MhHHJ2AP5joJpoKSVzakJzhnL9Ca4VHayjGENxpcAuHoNV18LS_VuB9wm_MdXmLT0UdnUBSmhZ4cO2bhu4kRErE4vXhJlG0Tzp5AgJoW_Rk; _cfuvid=m5mvZKub0jX9HgTeOKnRS9sZzNGvG24ZnapMC26NgsI-1725266087842-0.0.1.1-604800000'
                    }

                    # Todo: Fourth one is review requests
                    review_response = requests.request("POST", basket_url, headers=headers, data=payload)
                    if review_response.status_code != 200:
                        for rsr in range(3):
                            review_response = requests.request("POST", basket_url, headers=headers, data=payload)
                            if review_response.status_code == 200:
                                break
                    reviews_res = json.loads(review_response.text)
                    # path = f"C:\\Actowiz\\pagesave\\Deliveroo\\{formatted_date_pagesave}\\Review_COunt\\"
                    path = db.pagesave_review_count_path
                    if not os.path.exists(path):
                        os.makedirs(path)
                    file_name = path + vendor_id + ".html"
                    file_name = file_name.replace("\\", '\\\\')
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(review_response.text)
                    try:
                        rating_score = reviews_res['data']['reviewData']['layouts'][0]['ratingBreakdown'][
                            'averageRating']
                        number_of_ratings = len(reviews_res['data']['reviewData']['layouts'][1]['reviews'])
                    except:
                        rating_score = ""
                        number_of_ratings = ""
                    promotions = 1
                    promo = []
                    phone_details = json_data['props']['initialState']['menuPage']['menu']['layoutGroups']
                    for p in phone_details:
                        try:
                            p_data = p['layouts']
                            for pd in p_data:
                                mm_data = pd['header']
                                data2 = pd['subheader']
                                if mm_data:
                                    if " off selected items" in mm_data:
                                        promo.append(mm_data + " : " + data2)
                                try:
                                    prom = pd['carouselBlocks']
                                    for pi in prom:
                                        pro_text = ""
                                        type_text = pi['header']['typeName']
                                        if type_text == 'UITitleLine':
                                            pro_text_1 = pi['header']['text']
                                            pro_text_2 = pi['lines'][0]['spans'][0]['text']
                                            if "About" not in pro_text_1 and "Delivered by " not in pro_text_1 and " on Editions" not in pro_text_1:
                                                pro_text = pro_text_1 + " : " + pro_text_2
                                                promo.append(pro_text)
                                            else:
                                                other[pro_text_1.replace('"', "")] = pro_text_2.replace("\n",
                                                                                                        "").replace('"',
                                                                                                                    "").replace(
                                                    "\t", "").replace("'", "''")
                                    promotion_tags_delivery = " | ".join(promo)
                                    if promo != []:
                                        promotions = "1"
                                    else:
                                        promotions = "0"
                                except Exception as e:
                                    print(e)

                                pds = pd['blocks']
                                try:
                                    for b in pds:
                                        try:
                                            latitude = b['map']['pins'][0]['lat']
                                            longitude = b['map']['pins'][0]['lon']
                                        except Exception as e:
                                            print(e)
                                            block = b['actions']
                                            try:
                                                for l in block:
                                                    lock = l['target']['params']
                                                    for ll in lock:
                                                        data_id = ll['id']
                                                        if data_id == "phone":
                                                            phone_number = ll['value'][0]
                                            except Exception as e:
                                                print(e)
                                except  Exception as e:
                                    print(e)
                        except Exception as e:
                            print(e)

                    address = \
                    json_data['props']['initialState']['menuPage']['menu']['meta']['restaurant']['location']['address'][
                        'address1']
                    address_local = address
                    postal_code = \
                    json_data['props']['initialState']['menuPage']['menu']['meta']['restaurant']['location']['address'][
                        'postCode']
                    if postal_code == "None" or postal_code == None:
                        postal_code = ""
                    country_code = \
                    json_data['props']['initialState']['menuPage']['menu']['meta']['restaurant']['location']['address'][
                        'country']
                    city = \
                    json_data['props']['initialState']['menuPage']['menu']['meta']['restaurant']['location']['address'][
                        'city']
                    request_location_Latitude = \
                    json_data['props']['initialState']['menuPage']['menu']['meta']['customerLocation']['lat']
                    request_location_Longitude = \
                    json_data['props']['initialState']['menuPage']['menu']['meta']['customerLocation']['lon']
                    delivery_time_unit = ""
                    delivery_time = deliver_time(request_location_Latitude, request_location_Longitude, drn, vendor_id)
                    if delivery_time:
                        delivery_time_unit = "min"
                    now = datetime.now()

                    # Format the date in dd-mm-yyyy
                    formatted_date = now.strftime('%Y-%m-%d')
                    date_of_scrape = formatted_date
                    date_of_data_inserted = formatted_date

                    full_url = url.split("?")
                    fully_url = full_url[0] + "?fulfillment_method=collection&" + full_url[1]
                    full_headers = {
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                        'accept-encoding': 'gzip, deflate, br, zstd',
                        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
                        'cache-control': 'max-age=0',
                        'cookie': 'roo_guid=8138c8de-c351-45a8-b7cf-39c6d877b3e8; roo_guid=8138c8de-c351-45a8-b7cf-39c6d877b3e8; shield_FPC=SCfQ8I7q6gH6gM1LWepuUTvRu1gvnqfWv5; _pxvid=9a8a8160-66a0-11ef-9c06-8676d3121305; __pxvid=9aceaffc-66a0-11ef-aa68-0242ac120002; _gcl_au=1.1.1423357780.1725002548; _ga=GA1.1.750316016.1725002545; _scid=3abfdd1a-aef0-4a89-921e-eb4f595bd4da; _tt_enable_cookie=1; _ttp=JmQ5r8-_Sv04Uyd3hwHjXTlMvkt; _pin_unauth=dWlkPU5XUmhaakkzWkRrdE1qazJZaTAwWmpOaExUaGpabVF0T1dWaFltRmpOV1ZoWWpBMg; _ScCbts=%5B%5D; _fbp=fb.1.1725002549903.819407487304369002; _sctr=1%7C1724956200000; external_device_id=a2311f6a-7924-48c7-affa-b1349f4d8ee4; cwa_user_preferences={%22deviceStats%22:{%22innerWidth%22:1280}%2C%22seen_modals%22:{%22nc_promos_nux_2814ac7a-87db-4e08-858d-68f91c982634%22:{%22id%22:%22nc_promos_nux_2814ac7a-87db-4e08-858d-68f91c982634%22%2C%22timestamp%22:1725002571}%2C%22flash_deals%22:{%22id%22:%22flash_deals%22%2C%22timestamp%22:1725002730}}}; cf_clearance=ToRe_MsDNTn1RSX0iYIDhyCwSOVe6L7Mgzw4zHHyylk-1725003269-1.2.1.1-0X4dKIQdLYTqXbJiPoJroNL1FzyPSlPp8cK5pLm3KHtJakr_SDAtPNE_F2sP6Fi.GClqlG2WtwYwU2oqWK1Ob1hVntDsiCczfA0FuQQ4AvW_oN5HG4S2a79JXOcgUDslZ6q4E6u1z9I4cvOLz.vGGFsUywJqnijfMx2cNz3PYHwLi.ytGzmLr644U1va7ivmf7Adjh8SCDaPuU1CIE22ZNI_47tUrF3ZT0Nla0Fo4F900vEM9rQTozkcwm4.JzvzLWNOYOwwKbTJMDJO8j9g_TtwK3j2cI3S17kbXOLue6WemWnqi8EreJjSjoliHMTksdpfl5mtH.YNIY5Jffwn90Mnvl3kKyDRq_sH101o0bDZiNLiSweZszQuuFz.1FJRfpRtlpkc823BcgtimKzcANVuRQPmtFtcZEeyDtC6h3k; location_data=eyJsb2NhdGlvbiI6eyJjb29yZGluYXRlcyI6WzExNC4xNTkyNTk2LDIyLjI4NTIzMl0sImlkIjpudWxsLCJmb3JtYXR0ZWRfYWRkcmVzcyI6IlR3byBJbnRlcm5hdGlvbmFsIEZpbmFuY2UgQ2VudHJlLCA4IEZpbmFuY2UgU3QsIENlbnRyYWwsIEhvbmcgS29uZyIsInBsYWNlX2lkIjoiQ2hJSjYxaFpyR01BQkRRUlFxWWgzWXRadFA0IiwicGluX3JlZmluZWQiOmZhbHNlLCJjaXR5IjpudWxsfX0.; roo_session_guid=f2b91832-0d23-4325-bc76-fbe5e2d8f582; locale=eyJsb2NhbGUiOiJlbiJ9; pxcts=c43ac8d4-68ec-11ef-8308-f8eb2aa81e42; _clck=1dcfr8c%7C2%7Cfou%7C0%7C1703; roo_super_properties=eyJjb250ZXh0Ijp7InVzZXJBZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMjguMC4wLjAgU2FmYXJpLzUzNy4zNiIsImlwIjoiNS42Mi41Ni4yNTEiLCJsb2NhdGlvbiI6eyJjb3VudHJ5IjoiSG9uZyBLb25nIn0sImxvY2FsZSI6ImVuIn0sIlJlcXVlc3RlZCBMb2NhbGUiOiJlbiIsIlJvb0Jyb3dzZXIiOiJDaHJvbWUiLCJSb29Ccm93c2VyVmVyc2lvbiI6IjEyOCIsIkRldmljZSBUeXBlIjoiZGVza3RvcCIsIlRMRCI6ImhrIiwiUGxhdGZvcm0iOiJ3ZWIiLCJMb2NhbGUiOiJlbiIsIndoaXRlX2xhYmVsX2JyYW5kIjoiY29yZSJ9; _ga_ZW8Q7SZ57X=GS1.1.1725275857.9.1.1725276378.42.0.0; OptanonAlertBoxClosed=2024-09-02T11:26:18.525Z; _scid_r=3abfdd1a-aef0-4a89-921e-eb4f595bd4da; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+02+2024+16%3A56%3A20+GMT%2B0530+(India+Standard+Time)&version=202404.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=dd291773-4cd7-41da-8bfb-acfb3ffe8a34&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=H95%3A1%2CH5%3A1%2CH111%3A1%2CH79%3A1%2CH80%3A1%2CH86%3A1%2CH85%3A1%2CH4%3A1%2CH155%3A1%2CH74%3A1%2CH38%3A1%2CH89%3A1%2CH99%3A1%2CH108%3A1%2CH167%3A1%2CH20%3A1%2CH77%3A1%2CH164%3A1%2CH156%3A1%2CH101%3A1%2CH104%3A1%2CH25%3A1%2CH162%3A1%2CH83%3A1%2CH39%3A1%2CH159%3A1&genVendors=&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false; _uetsid=c51c056068ec11efb96a498dddceabbc; _uetvid=9d34e33066a011efae244b85347c60fb; _clsk=1u7nqrx%7C1725277698981%7C13%7C0%7Cn.clarity.ms%2Fcollect; __cf_bm=hh8JpphujQDmiBMYNmWmZ0p8BDUSpbI1d3kVhkODkRw-1725277848-1.0.1.1-okWsmbsJ2iBtJ9GcR0wJk4Gyb7at2YvKeszhdyOC0m7CMpfAk5VpK.3he2mTDPO9Ai.kK11QBCvfVtd6PHhtkj3pVF7ztI9gMejiQimgyZY; external_device_id=a2311f6a-7924-48c7-affa-b1349f4d8ee4; locale=eyJsb2NhbGUiOiJlbiJ9; roo_guid=8138c8de-c351-45a8-b7cf-39c6d877b3e8',
                        'priority': 'u=0, i',
                        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                        'sec-ch-ua-arch': '"x86"',
                        'sec-ch-ua-bitness': '"64"',
                        'sec-ch-ua-full-version': '"128.0.6613.113"',
                        'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.113", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.113"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-model': '""',
                        'sec-ch-ua-platform': '"Windows"',
                        'sec-ch-ua-platform-version': '"10.0.0"',
                        'sec-fetch-dest': 'document',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-user': '?1',
                        'upgrade-insecure-requests': '1',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
                    }
                    fully_response = requests.request("GET", fully_url, headers=full_headers, data=payload)
                    if fully_response.status_code != 200:
                        for frr in range(3):
                            fully_response = requests.request("GET", fully_url, headers=full_headers, data=payload)
                            if fully_response.status_code == 200:
                                break

                    # formatted_date1 = now.strftime('%Y_%m_%d')

                    fully_response = HtmlResponse(body=fully_response.text, url=url, encoding='utf-8')
                    # path = f"C:\\Actowiz\\pagesave\\Deliveroo\\{formatted_date_pagesave}\\Collection_Request\\"
                    path = db.pagesave_collection_request_path
                    if not os.path.exists(path):
                        os.makedirs(path)
                    file_name = path + vendor_id + ".html"
                    file_name = file_name.replace("\\", '\\\\')
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(fully_response.text)
                    full_data_json = fully_response.xpath('//script[@type="application/json"]//text()').get()
                    full_json_data = json.loads(full_data_json)
                    final_desc = full_json_data['props']['initialState']['menuPage']['menu']['layoutGroups']
                    final_prom = []
                    for ff in final_desc:
                        try:
                            full2 = ff['layouts']
                            for r3 in full2:
                                mm_data1 = r3['header']
                                mm_data2 = r3['subheader']
                                if mm_data1:
                                    if " off selected items" in mm_data1:
                                        final_prom.append(mm_data1 + " : " + mm_data2)
                                try:
                                    disc = r3['carouselBlocks']
                                    for d in disc:
                                        try:
                                            head = d['header']['typeName']
                                            if head == "UITitleLine":
                                                promotion_tags_pickup_1 = d['header']['text']
                                                pro_text_pickup2 = d['lines'][0]['spans'][0]['text']
                                                if "About" not in promotion_tags_pickup_1 and "Delivered by " not in promotion_tags_pickup_1 and " on Editions" not in promotion_tags_pickup_1:
                                                    pro_text12 = promotion_tags_pickup_1 + " : " + pro_text_pickup2
                                                    final_prom.append(pro_text12)
                                        except  Exception as e:
                                            print(e)
                                except  Exception as e:
                                    print(e)
                        except Exception as e:
                            print(e)
                    promotion_tags_pickup = " | ".join(final_prom)
                    if pop_list != []:
                        popular = "Popular with other people"
                        other[popular] = pop_list
                    try:
                        others = json.dumps(other, ensure_ascii=False, )
                    except Exception as e:
                        print(e)
                    if category != "":
                        item = DeliverooItem()
                        item['vendor_id'] = vendor_id
                        item['lead_source'] = lead_source
                        item['name'] = name
                        item['name_local'] = name_local
                        item['branch_name'] = branch_name
                        item['branch_name_local'] = branch_name_local
                        item['type'] = type
                        item['category'] = category
                        item['scraped_url'] = scraped_url
                        item['restaurant_url'] = restaurant_url
                        item['cuisine'] = cuisine
                        item['phone_number'] = phone_number
                        item['opening_hours'] = opening_hours
                        item['rating_score'] = rating_score
                        item['number_of_ratings'] = number_of_ratings
                        # item['food_license_number'] = food_license_number
                        item['country_code'] = country_code
                        item['city'] = city
                        item['address'] = address
                        item['address_local'] = address_local
                        item['postal_code'] = postal_code
                        item['latitude'] = latitude
                        item['longitude'] = longitude
                        # item['request_location'] = request_location
                        item['promotions'] = promotions
                        # item['payment_method'] = payment_method
                        item['minimum_order_price'] = minimum_order_price
                        item['free_delivery_option'] = free_delivery_option
                        item['delivery_fee'] = delivery_fee
                        item['distance'] = distance
                        item['distance_unit'] = distance_unit
                        item['delivery_time'] = delivery_time
                        item['delivery_time_unit'] = delivery_time_unit
                        item['others'] = others
                        item['promotion_tags_delivery'] = promotion_tags_delivery
                        item['promotion_tags_pickup'] = promotion_tags_pickup
                        item['date_of_scrape'] = date_of_scrape
                        item['date_of_data_inserted'] = date_of_data_inserted
                        item['is_open'] = is_open
                        item['is_delivery_available'] = is_delivery_available
                        item['is_pickup_enabled'] = is_pickup_enabled
                        item['request_location_Latitude'] = request_location_Latitude
                        item['request_location_Longitude'] = request_location_Longitude
                        yield item
                    else:
                        update_d = current_date.strftime("%Y_%m_%d")
                        sql = f"update {db.restaurant_links} set `status`='Store'  where vendor_id={vendor_id};"
                        mycursor.execute(sql)
                        mydb.commit()
                else:
                    update_d = current_date.strftime("%Y_%m_%d")
                    sql = f"update {db.restaurant_links} set `status`='NF'  where vendor_id={vendor_id};"
                    mycursor.execute(sql)
                    mydb.commit()
            else:
                update_d = current_date.strftime("%Y_%m_%d")
                sql = f"update {db.restaurant_links} set `status`='404'  where vendor_id={vendor_id};"
                mycursor.execute(sql)
                mydb.commit()


if __name__ == '__main__':
    execute("scrapy crawl data -a a=0 -a b=150".split())
