function create(type){
        let content = document.querySelector('#postbox').value;
        console.log(content)
        fetch(`create/${type}`, {
          method: 'POST',
          body: JSON.stringify({
            'content': content
        })
        })
          .then(response => response.json())
          .then(data => {
            if (data.success) {
              console.log(data.success)
            } else {
              console.log(data.error)
            }
          })
          .catch(error => console.error('Error:', error));
          window.location.reload()

}
function edit(id, type){
        let post = document.getElementById(`edit${type}${id}`).value;
        let currentpost = document.getElementById(`${type}-content${id}`);
        fetch(`/edit/${type}/${id}`,{
          method: 'POST',
          body: JSON.stringify({
            'content': post
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            currentpost.innerHTML = `<p id="content${id}">${post}</p>`
          } else {
            console.log(data.error)
          }
        })
        .catch(error => console.error('Error:', error));
}
function delete_item(id, type){
        let item = document.getElementById(`${type}${id}`)
        confirm('Are you sure you want to delete this post?')
        fetch(`/delete/${type}/${id}`,{
          method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            item.style.display = 'none'
          } else {
            console.log(data.error)
          }
        })
}
function like(id, type){
        let liker = document.getElementById(`like_post${id}`)
        let like_count = document.getElementById(`like_count${id}`)
          fetch(`/like/${type}/${id}`,{
              method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
              if (data.liked) {
                liker.innerHTML = '<i style="color: red;" class="fa-solid fa-heart"></i>'
              } else {
                liker.innerHTML = '<i style="color: red;" class="fa-regular fa-heart"></i>'
              }
              like_count.textContent = data.like_count
            })
            .catch(error => console.error('Error:', error));
}
function toggleedit(id, type){
  let content = document.getElementById(`content${id}`).textContent;
  let currentpost = document.getElementById(`${type}-content${id}`);
  // let new_content = document.getElementById(`editbox${id}`);
  // new_content.value = content
  currentpost.innerHTML = `
    <form>
      <textarea id="edit${type}${id}" class="postbox" name="post_text" rows="4" cols="50" required>${content}</textarea>
      <div class="createbutton">
          <input type="button" value="Post" onclick="edit('${id}','${type}')">
      </div>
  </form>
  `
}
function follow(type){
  let follower = document.getElementById(`follow`)
  let follow_count = document.getElementById(`follow_count`)
  let current_count= parseInt(document.getElementById(`follow_count`).textContent)
  for(post in follower)
  console.log(current_count)
  fetch(`${type}`,{
      method: 'POST',
  })
  .then(response => response.json())
  .then(data => {
    if (data.follow) {
      follower.innerHTML =`<button onclick="follow('unfollow')">Unfollow</button>`
      follow_count.textContent = `${current_count + 1}`
    } else {
      follower.innerHTML = `<button onclick="follow('follow')">Follow</button>`
      follow_count.textContent = `${current_count - 1}`
    }
  })
  .catch(error => console.error('Error:', error));
}