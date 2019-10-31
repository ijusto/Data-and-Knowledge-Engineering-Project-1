(:Todos os filmes de um ator:)

declare function local:get_movies_by_actor($a_first_name as xs:string, $a_last_name as xs:string) as element()*{
  <movies>{
  for $movie in  doc("moviesDB")//movie
    for $actors in $movie//main_actors//person
      where $actors/first_name=$a_first_name and $actors/last_name=$a_last_name
      return $movie
  }</movies>
};

(: Todos os atores de um filme)