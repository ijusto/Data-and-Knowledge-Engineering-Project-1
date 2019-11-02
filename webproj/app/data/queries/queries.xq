(: GET ALL functions :)
declare function local:get_all_genres() as element()*{
  let $genres := doc("moviesDB")//genres
  for $genre in distinct-values($genres/genre)
  return <text>{$genre}</text>
};

declare function local:get_all_plot_keywords() as element()*{
    let $plot_keywords := doc("moviesDB")//plot_keywords
    for $key_word in distinct-values($plot_keywords/keyword)
    return <text>{ $key_word }</text>
};

declare function local:get_all_actors() as item(){
  <actors>{
    let $people := doc("moviesDB")//person
    for $person in $people
    where matches(data($person//profession), "Actor")
    return $person
  }</actors>
};

(: Get specific functions :)
(: Every movie of an actor :)
declare function local:get_movies_by_actor($a_first_name as xs:string, $a_last_name as xs:string) as element()*{
  <movies>{
  for $movie in  doc("moviesDB")//movie
    for $actors in $movie//main_actors//person
      where $actors//first_name=$a_first_name and $actors//last_name=$a_last_name
      return $movie
  }</movies>
};

(: Every actor of a movie :)
declare function local:get_actors_by_movie($movie_name as xs:string) as element()*{

  let $movie:= doc("moviesDB")//movie[title/name=$movie_name]
  return $movie//main_actors

};

(: Every movie of a director :)
declare function local:get_movies_by_director($dir_first_name as xs:string, $dir_last_name as xs:string) as element()*{
  for $movie in doc("moviesDB")//movie
  where $movie//director//first_name=$dir_first_name and $movie//director//last_name=$dir_last_name
  return $movie
};

(: SELECT functions :)
(: Every genre selected :)
declare function local:selected_genres($m, $g) as item(){
    let $movies := doc($m)
    let $genres := doc($g)

    for $movie in $movies//movie
        for $m_genre in $movie//genre
            for $q_genre in $genres//genres
                where matches(data($q_genre), data($m_genre))
                return  if (data($genres//genre)="") then
                            $movies
                        else
                            $movie
};

declare function local:selected_rating($m, $r) as item(){
    let $movies := doc($m)
    let $rating := doc($r)
    for $movie in $movies//movie
        where matches(data($movie//@rating), data($rating//rating))
        return if (data($rating//rating)="") then
                    $movies
               else
                    $movie
};

declare function local:selected_year($m, $y) as item(){
    let $movies := doc($m)
    let $year := doc($y)
    for $movie in $movies//movie
        where matches(data($movie//year), data($year//year))
        return if (data($year//year)="") then
                    $movies
               else
                    $movie
};

declare function local:selected_categories($xml) as item(){
    (: <query>  <genres>  <genre></genre>  </genres>    <rating></rating>    <year></year>  </query> :)
    let $query := doc($xml)
    let $movies := doc(moviesDB)
    return  local:selected_year(local:selected_rating(local:selected_genres($movies, $query), $query), $query)
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

local:get_all_genres()