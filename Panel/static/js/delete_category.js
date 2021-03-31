function deleteCategory(cat_id) {
    $.ajax({
        url:"/panel/ajax/delete-category/",
        type:'POST',
        data:{
            id :cat_id,
        },
        success:function (data) {
            if (data["Status"]=="Success"){
                location.reload();
            }
        }
    })
}