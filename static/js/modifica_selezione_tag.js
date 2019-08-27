tag_primario=$("#tag_primario_scelto").val();
$("#tag_prim_"+tag_primario).prop("checked", true);

tag_secondari=$("#tag_secondari_scelti").val();
for (tag_id of tag_secondari.split(",")){
    $("#tag_"+tag_id).prop("checked", true);
}