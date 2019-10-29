let $plot_keywords := collection("../movies.xml")//plot_keywords
for $key_word in distinct-values($plot_keywords/keyword)
return $key_word