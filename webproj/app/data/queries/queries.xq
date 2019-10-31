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

(: UPDATE xml functions :)
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





