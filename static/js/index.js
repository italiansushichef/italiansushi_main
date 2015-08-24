$(document).ready(function() {
        $("div.bhoechie-tab-menu>div.list-group>a").click(function(e) {
                e.preventDefault();
                $(this).siblings('a.active').removeClass("active");
                $(this).addClass("active");
                var index = $(this).index();
                $("div.bhoechie-tab>div.bhoechie-tab-content").removeClass("active");
                $("div.bhoechie-tab>div.bhoechie-tab-content").eq(index).addClass("active");
            });
        });

        $('.login-popup').click(function(e){
            e.preventDefault();
            console.log("login-btn clicked");
            bootbox.dialog({
                
                message: '<div class="row">'
                            + '<div class="col-xs-12">'
                                + '<h1 class="text-center form-title"> Log in to upload, save, and download item sets. </h1>'
                                + '<div class="form-box">'
                                    + '<form id="login-form" class="form-login" method="POST" action="/login/">'
                                        + "{% csrf_token %}" 
                                        + '<input type="text" name="usernameoremail" class="form-control" placeholder="Username or Email" required autofocus>'
                                        + '<input type="password" name="password" class="form-control" placeholder="Password" required>'
                                        + '<button type="submit" class="hide" id="submit-login-form"></button>'
                                    + '</form>'
                                + '</div>'
                            + '</div>'
                        + '</div>',
                buttons: {
                    success: {
                        label: "Log In",
                        className: "btn-primary",
                        callback: function(){
                            $('#submit-login-form').click();
                            return false;
                        }
                    }
                }
            });
        });

        $('.createuser-popup').click(function(e){
            e.preventDefault();
            console.log("createuser-btn clicked");
            bootbox.dialog({
                
                message: '<div class="row">'
                            + '<div class="col-xs-12">'
                                + '<h1 class="text-center form-title"> Create a free user account to upload, save, and download item sets. Please note this account is separate from your Riot League of Legends account. </h1>'
                                + '<div class="form-box">'
                                    + '<form id="createuser-form" class="form-login" method="POST" action="/createuser/">'
                                        + "{% csrf_token %}" 
                                        + '<input type="text" name="username" class="form-control" placeholder="Username" required autofocus>'
                                        + '<input type="text" name="email" class="form-control" placeholder="Email" required>'
                                        + '<input type="password" name="password" class="form-control" placeholder="Password" required>'
                                        // + '<input type="password" name="repassword" class="form-control" placeholder="Re-enter Password" required>'
                                        + '<button type="submit" class="hide" id="submit-createuser-form"></button>'
                                    + '</form>'
                                + '</div>'
                            + '</div>'
                        + '</div>',
                buttons: {
                    success: {
                        label: "Create User Account",
                        className: "btn-primary",
                        callback: function(){
                            $('#submit-createuser-form').click();
                            return false;
                        }
                    }
                }
            });
        });
        
        $('.viewfiles-popup').click(function(e){
            e.preventDefault();
            // console.log("viewfiles-btn clicked");
            var items = []; 
            $.when($.get('/view-items/', function(result){
                tmp = result.split('>>');
                numitems = parseInt(tmp[0]);
                // console.log(tmp);
                var i;
                for (i = 1; i <= numitems; i++)
                {
                    items.push(tmp[i]);
                    // console.log("pushed " + tmp[i])
                }
                // console.log("items before " + items);
            })).then(function(){
                // console.log("items after1 " + items);
                bootbox.dialog({
                    
                    message: '<div class="row">'
                                + '<div class="col-xs-12">'
                                    + '<h1 class="text-center form-title"> View, Download, and Delete your Item Sets </h1>'
                                    + '<div class="panel panel-default">'
                                        + '<div class ="panel-body" id="dynamic-panel">'
                                        + '</div>'
                                    + '</div>'
                                + '</div>'
                            + '</div>',
                });
                var dynamictable;
                if (items.length == 0)
                {
                    dynamictable = '<h4> No item sets currently saved </h4>';
                }
                else
                {
                    dynamictable = '<table class="table"><col width="80%"><col width="10%"><col width="10%">';
                    // Head
                    dynamictable += '<thead>';
                    dynamictable += '<tr><th>ItemSet</th><th class="text-center">Download</th>';
                    dynamictable += '<th class="text-center">Delete</th></tr>';
                    dynamictable += '</thead>';
                    // Body
                    dynamictable += '<tbody>' ;
                    for (var i = 0; i < items.length; i++)
                    {
                        dynamictable += '<tr id="row_' + items[i] + '">';
                        dynamictable += '<td>' + items[i] + '</td>';
                        dynamictable += '<td class="text-center"><a href="/{{user.username}}/' + items[i] + '.json"' 
                                        + ' type="submit" class="btn btn-success"' 
                                        + 'id="{{user.username}}_dl_' + items[i] +'" target="_blank">'
                                        + '<span class="fa fa-download"></span></a></td>';

                        dynamictable += '<td class="text-center">'
                                        + '<form method="POST" action="" id="{{user.username}}_delete_'+items[i]+'_form">' 
                                        + "{% csrf_token %}"
                                        + '<input type="text" name="name" value="'+items[i]+'" hidden = true/>'
                                        + '<input type="text" name="user" value="{{user.username}}" hidden = true/>'
                                        + '<button type="submit" class="btn btn-danger btn-delete-item"'
                                        + 'id="{{user.username}}_delete_' + items[i]+'">'
                                        + '<span class="fa fa-trash-o"></span></button></form></td>';
                        dynamictable += '</tr>';
                    }

                    dynamictable += '</tbody>';
                    dynamictable += '</table>';
                }
                document.getElementById('dynamic-panel').innerHTML = dynamictable;
                // console.log("items after2 " + items);

                $('.btn-delete-item').click(function(e){
                    e.preventDefault();
                    var id = (e.currentTarget.id || e.srcEvent.id); // this may not work in IE!
                    var clicked_btn = document.getElementById(id);                    
                    var clicked_btn_id = clicked_btn.id.split('_');
                    var itemset_name = clicked_btn_id[2];
                    for (var i = 3; i < clicked_btn_id.length; i++)
                    {
                        itemset_name += "_" + clicked_btn_id[i];
                    }
                    var delete_form_id = clicked_btn.id + '_form';
                    var delete_form = document.getElementById(delete_form_id);
                    var confirmation_message = "Are you sure you want to remove " + itemset_name + "?";
                    bootbox.confirm(confirmation_message, function(result) {
                        if (result) {
                            var parentrow = $(clicked_btn.parentNode.parentNode.parentNode); // hardcoded for current structure
                            parentrow.remove();
                            $.post('/delete-itemset/', $(delete_form).serialize(), function(response){
                                console.log(response);
                            });
                        }
                    });
                    
                });
            });       
        });

        /* gets the URL parameters, i.e. http://dummy.com/?technology=jquery&blog=jquerybyexample 
            -- var tech = getUrlParameter('technology'); */  
        var getUrlParameter = function getUrlParameter(sParam) {
            var sPageURL = decodeURIComponent(window.location.search.substring(1)),
                sURLVariables = sPageURL.split('&'),
                sParameterName,
                i;

            for (var i = 0; i < sURLVariables.length; i++) {
                sParameterName = sURLVariables[i].split('=');

                if (sParameterName[0] === sParam) {
                    return sParameterName[1] === undefined ? true : sParameterName[1];
                }
            }
            return null;
        };

        console.log("upload= " + getUrlParameter('upload'));