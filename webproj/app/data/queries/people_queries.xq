module namespace people = "com.people";

(: $actor = <actor>Brad Pitt</actor>:)
declare function people:get_img($actor) as element()*{
  for $name in doc("peopleDB")//name
  where matches(data($name), data($actor))
  return $name/../img
};
(: $actor = <actor>Brad Pitt</actor>:)
declare function people:get_bio($actor) as element()*{
  for $name in doc("peopleDB")//name
  where matches(data($name), data($actor))
  return $name/../bio
};