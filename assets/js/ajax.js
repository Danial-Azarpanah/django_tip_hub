// Ajax function for adding or removing a video to favorites
function fav_add_del(id) {
            var element = document.getElementById('favorite')
            $.get(`/account/add-favorite/${id}`).then(response =>
                {
                if (response["response"] === "added") {
                    console.log("deleted")
                    element.className = 'fa fa-bookmark'
                } else {
                    console.log("added")
                    element.className = 'fa fa-bookmark-o'
                }
            })
        }