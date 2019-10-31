let $plot_keywords := fn:collection("../movies.xml")//plot_keywords
for $key_word in fn:distinct-values($plot_keywords/keyword)
return $key_word