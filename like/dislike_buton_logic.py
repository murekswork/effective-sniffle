# document.addEventListener('DOMContentLoaded', function () {
#                     var dislikeButton = document.querySelector('.heart-dislike-button');
#
#                     dislikeButton.addEventListener('click', function () {
#                         dislikeButton.classList.toggle('disliked')
#
#                         if (dislikeButton.classList.contains('disliked')) {
#                             setTimeout(function () {
#                                 dislikeButton.classList.remove('disliked')
#                             }, 1500)
#                         }
#                     });
#                 });
#
# $('#ajax-dislike-button').click(ajaxSenddislike)
#
#                     function  ajaxSenddislike() {
#                         let profile_pk = document.getElementById('ajax-dislike-button').value
#                         let dislike_url = 'http://127.0.0.1:8000/dislike/'
#                         $.ajax({
#                             url: dislike_url + profile_pk,
#                             success: change_profile
#
#                         })
#                     }