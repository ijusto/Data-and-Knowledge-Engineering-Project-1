(: Get ALL functions :)
declare function local:get_genres() as item(){
    <genres>{
        let $genres := doc("moviesDB")//genres
        for $genre in distinct-values($genres/genre)
        return <genre>{ $genre }</genre>
    }</genres>
};

declare function local:get_plot_keywords() as item(){
    <plot_keywords>{
        let $plot_keywords := doc("moviesDB")//plot_keywords
        for $key_word in distinct-values($plot_keywords/keyword)
        return <keyword>{ $key_word }</keyword>
    }</plot_keywords>
};

declare function local:get_all_actors() as item(){

};

(: UPDATE DB functions :)
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

(: Get specific functions :)


(: Select functions :)
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



