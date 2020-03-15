//Add Comment Using Ajax With Django
$(document).on('click','#addNewComment',function(e){
    // To Prevent Page Refresh
    e.preventDefault();
    $.ajax({
        type : "POST",
        url : 'http://localhost:8000/project/addcomment',
        data:{
            project_id : '{{project.p_id}}',
            user_id : "1",
            comment_content : $("input[name='commentContent']").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(data)
        {
            $("input[name='commentContent']").val("")
            let object = JSON.parse(data["data"]);
            let fields = object[0]["fields"];
            let commentBody = fields.comment_body;
            let username = data.username;
            let user_img = data.user_img
            var html = '<div class="userCommentsContainer" style="width: 100%;">'+
                            '<div class="userComment">'+
                                '<img class="commentImg" src="{% static '/image/'%}'+user_img+'">'+
                                '<p class="usernameComment" style="font-weight:bold ">'+username+'</p>'+
                                '<div class="commentControllers">'+
                                    '<a href="" class="btn btn-danger commentEdit" >Report</a>'+
                                '</div>'+
                                '<p class="commentContent lead header">'+commentBody+'</p>'+
                            '</div>'+
                        '</div>';
            $("#PostContainer").append(html);
        }
    })
});

// Add Project Report Using Ajax
$(document).on("click","#projectReport",function(e){
    e.preventDefault();
    $.ajax({
        type : "POST",
        url : 'http://localhost:8000/project/report',
        data:{
            project_id : '{{project.p_id}}',
            user_id : "1",
            report_text : $("#report_text").val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(data)
        {
            $("#report_text").val("");
            var html = '<p style="color: #009E74;font-weight: bold;">'+
                            'Thank You For Your Report We Will Review It Soon'+
                        '</p>';
            $(".modal-body").append(html);
            setTimeout(function() {
                $('#exampleModal').modal('hide');
            }, 2000);
        }
    })
});