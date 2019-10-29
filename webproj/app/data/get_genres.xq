let $g := collection("movies.xml")//genres
for $c in distinct-values($g/genre)
return $c