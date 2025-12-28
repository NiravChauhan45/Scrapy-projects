-- men - Topwear
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'men' AND category_name = 'Topwear'
AND sub_category_name IN ("T-Shirts","Sweatshirts","Polo T-Shirts","Formal Shirts","Casual Shirts","Sweaters","Hoodies","Jackets","Blazers & Coats"));

-- men - Bottomwear 
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'men' AND category_name = 'Bottomwear'
AND sub_category_name IN ("Jeans","Casual Trousers","Formal Trousers","Shorts","Trackpants"));

-- men - Ethnicwear
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'men' AND category_name = 'Ethnicwear'
AND sub_category_name IN ("Dhoti Sets","Nehru Jackets","Sherwanis"));


-- men - Innerwear & Sleepwear
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'men' AND category_name = 'Innerwear & Sleepwear'
AND sub_category_name IN ("Pyjama & Pyjama Sets"));

-- men - Active & Sports
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'men' AND category_name = 'Active & Sports'
AND sub_category_name IN ("T-Shirts & Tanks","Shorts","Tracksuits"));




-- women - Indianwear
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'women' AND category_name = 'Indianwear'
AND sub_category_name IN ("Kurtis Kurtas & Tunics","Sarees","Lehengas","Salwar Suits & Sets","Dupattas"));

-- women - Westernwear
INSERT IGNORE INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'women' AND category_name = 'Westernwear'
AND sub_category_name IN ("Dresses","Tops","T-shirts","Shirts","Jeans & Jeggings","Bottoms Pants & Trousers","Skirts","Jumpsuits"));

-- women - Lingerie
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'women' AND category_name = 'Lingerie'
AND sub_category_name IN ("Sleepwear"));

-- women - Active & Sports
INSERT INTO `new_category_links`(SELECT * FROM `cat_links`
WHERE main_category_name = 'women' AND category_name = 'Active & Sports'
AND sub_category_name IN ("Leggings & Tights","Track Pants & Joggers","Jackets"));


