module namespace movies = "com.movies";

(: GET ALL functions :)
declare function movies:get_all_genres() as element()*{
  let $genres := doc("moviesDB")//genres
  for $genre in distinct-values($genres/genre)
  return <genre>{$genre}</genre>
};

declare function movies:get_all_ratings() as element()*{
  for $rating in distinct-values(doc("moviesDB")//@rating)
  return <rating>{$rating}</rating>
};

declare function movies:get_all_years() as element()*{
  for $year in distinct-values(doc("moviesDB")//year)
  order by $year
  return <year>{$year}</year>
};

declare function movies:get_all_plot_keywords() as element()*{
    let $plot_keywords := doc("moviesDB")//plot_keywords
    for $key_word in distinct-values($plot_keywords/keyword)
    return <text>{ $key_word }</text>
};

declare function movies:get_all_actors() as element()*{
  <actors>{
    let $people := doc("moviesDB")//person
    for $person in $people
    where matches(data($person//profession), "Actor")
    return $person//name
  }</actors>
};

declare function movies:get_all_directors() as element()*{
  <directors>{
    let $people := doc("moviesDB")//person
    for $person in $people
    where matches(data($person//profession), "Movie Director")
    return $person//name
  }</directors>
};

declare function movies:get_imdb_link($firstname, $lastname) as element()*{
    <links>{
        let $movies := doc("moviesDB")//movie
        for $movie in $movies
            for $name in $movie//person/name
            where matches(data($name/first_name), $firstname) and
                  matches(data($name/last_name), $lastname)
            return <link>{$movie//link}</link>
    }</links>
};

(: Get specific functions :)
(: Every movie of an actor :)
declare function movies:get_movies_by_actor($a_first_name as xs:string, $a_last_name as xs:string) as item(){
  <movies>{
  for $movie in  doc("moviesDB")//movie
    for $actors in $movie//main_actors//person
      where $actors//first_name=$a_first_name and $actors//last_name=$a_last_name
      return $movie
  }</movies>
};

(: Every actor of a movie :)
    (:1. No caso de escolhermos não haver atores secundários:)
declare function movies:get_actors_by_movie($movie_name as xs:string) as element()*{

  let $movie:= doc("moviesDB")//movie[title/name=$movie_name]
  return $movie//main_actors

};
    (:2. No caso de escolhermos haver atores secundários :)
(:declare function movies:get_actors_by_movie($movie_name as xs:string) as item(){
  <actors>{
    let $movie:= doc("moviesDB")//movie[title/name=$movie_name]
    return
      if (exists($movie//secondary_actors)) then
        $movie//main_actors and $movie//secondary_actors
      else
        $movie//main_actors
  }</actors>
};
:)

(: Every movie of a director :)
declare function movies:get_movies_by_director($dir_first_name as xs:string, $dir_last_name as xs:string) as item(){
  <movies>{
      for $movie in doc("moviesDB")//movie
      where $movie//director//first_name=$dir_first_name and $movie//director//last_name=$dir_last_name
      return $movie
  }</movies>
};

(: Every movie that starts with a letter :)
declare function movies:get_movies_by_first_letter($letter) as item(){
  <movies>{
    for $movie in doc("moviesDB")//movie
    where starts-with($movie/title/name, $letter)
    return  $movie
  }</movies>
};

(: Year of a specific movie :)
declare function movies:get_movie_year($movie_name as xs:string) as item(){
  let $movie := doc("moviesDB")//movie[title/name=$movie_name]
  return $movie//year
};

(: Genres of a specific movie :)
declare function movies:get_movie_genres($movie_name as xs:string) as element()*{
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    for $genre in $movie//genre
      return $genre
};

(: Director of a specific movie :)
declare function movies:get_movie_director_name($movie_name as xs:string) as item(){
  let $movie := doc("moviesDB")//movie[title/name=$movie_name]
  return string-join(($movie/director//first_name/text(), $movie/director//last_name/text())," ")
};

(: Main actors of a specific movie :)
declare function movies:get_movie_main_actors($movie_name as xs:string) as element()*{
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    for $actor in $movie//main_actors//name
      return <actor>{string-join(($actor/first_name/text(), $actor/last_name/text())," ")}</actor>
};

(: Score of a specific movie :)
declare function movies:get_movie_score($movie_name as xs:string) as item(){
  let $movie := doc("moviesDB")//movie[title/name=$movie_name]
  return <score>{$movie//score/text()}</score>
};

(: Duration of a specific movie :)
declare function movies:get_movie_duration($movie_name as xs:string) as item(){
    let $movie := doc("moviesDB")//movie[title/name=$movie_name]
    return <duration>{data($movie/@duration)}</duration>
};


(: SELECT functions :)
(: Every genre selected :)
declare function movies:selected_genres($genres) as element()*{
    <movies>{
      let $movies := doc("moviesDB")     
      return if (data($genres//genre[1])="") then
                  for $movie in $movies//movie
                  return $movie
             else
                  for $movie in $movies//movie
                    for $m_genre in $movie//genre
                        for $q_genre in $genres//genre
                        where matches(data($q_genre), data($m_genre))
                        return $movie
    }</movies>
};

declare function movies:selected_rating($rating) as element()*{
    <movies>{
      let $movies := doc("moviesDB")    
      return if  (data($rating//rating)="") then
                  for $movie in $movies//movie
                  return $movie
             else
                  for $movie in $movies//movie
                  where matches(data($movie//@rating), data($rating//rating))
                  return $movie
    }</movies>
};

declare function movies:selected_year($year) as element()*{
    <movies>{
      let $movies := doc("moviesDB")    
      return if (data($year//year)="") then
                  for $movie in $movies//movie
                  return $movie
             else
                  for $movie in $movies//movie
                  where matches(data($movie//year), data($year//year))
                  return $movie
    }</movies>
};

declare function movies:selected_filters($query) as element()*{
(: <query>  <genres>  <genre></genre>  </genres>    <rating></rating>    <year></year>  </query> :)
    <movies>{
        let $movies := doc("moviesDB")
        let $selected_movies_by_year := movies:selected_year($query)
        let $selected_movies_by_rating := movies:selected_rating($query)
        let $selected_movies_by_genres := movies:selected_genres($query)
        for $movie_y in $selected_movies_by_year//movie
        for $movie_r in $selected_movies_by_rating//movie
        for $movie_g in $selected_movies_by_genres//movie
        where matches(data($movie_y//title/name), data($movie_r//title/name))
                and matches(data($movie_g//title/name), data($movie_r//title/name))
        return $movie_g
    }</movies>
};

(: UPDATE DB functions :)
(:
declare function local:update_names() as item(){
    let $people := doc("moviesDB")//person
    for $person in $people
        let $first_name := $person/first_name
        let $last_name := $person/last_name
        return (
            insert node <name>
                {$first_name}{$last_name}
            </name> as first into $person
            ,
            delete node $person/first_name,
            delete node $person/last_name
      )
};
:)
(:movies:selected_filters(<query><genres><genre>Action</genre><genre>Comedy</genre></genres><rating>PG-13</rating><year>2009</year></query>):)
