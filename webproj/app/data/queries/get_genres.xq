let $genres := collection("../movies.xml")//genres
for $genre in distinct-values($genres/genre)
return $genre