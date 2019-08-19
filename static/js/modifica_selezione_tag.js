tag_primario=document.getElementById("tag_primario_scelto").value;
document.getElementById("tag_prim_"+tag_primario).checked = true;

tag_secondari=document.getElementById("tag_secondari_scelti").value;
for (tag_id of tag_secondari.split(",")){
    document.getElementById("tag_"+tag_id).checked = true;
}