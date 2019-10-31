(: Todos os filmes de um ator :)

declare function local:get_movies_by_actor($a_first_name as xs:string, $a_last_name as xs:string) as element()*{
  <movies>{
  for $movie in  doc("moviesDB")//movie
    for $actors in $movie//main_actors//person
      where $actors//first_name=$a_first_name and $actors//last_name=$a_last_name
      return $movie
  }</movies>
};

(: Todos os atores de um filme :)

declare function local:get_actors_by_movie($movie_name as xs:string) as element()*{

  let $movie:= doc("moviesDB")//movie[title/name=$movie_name]
  return $movie//main_actors

};

(: Todos os filmes de um determinado director :)

declare function local:get_movies_by_director($dir_first_name as xs:string, $dir_last_name as xs:string) as element()*{
  for $movie in doc("moviesDB")//movie
  where $movie//director//first_name=$dir_first_name and $movie//director//last_name=$dir_last_name
  return $movie
};