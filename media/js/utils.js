tinyMCE.init({
        // General options
        mode: "textareas",
        theme: "advanced",
        plugins:
        "pagebreak,style,layer,table,advhr,advimage,advlink,iespell,inlinepopups,insertdatetime,preview,searchreplace,contextmenu,paste,directionality,fullscreen,noneditable,xhtmlxtras,template",
        theme_advanced_buttons1:
        "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,fontselect,fontsizeselect",
        theme_advanced_buttons2 :
        "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,image",
        theme_advanced_buttons3 :
        "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,iespell,advhr,|,fullscreen",
        theme_advanced_toolbar_location: "top",
        theme_advanced_toolbar_align: "left",
        theme_advanced_statusbar_location: 'bottom',
        theme_advanced_path: false,
        theme_advanced_resize_horizontal: false,
        theme_advanced_resizing_use_cookie: true,
        theme_advanced_resizing: true,
});


function highlight_active() {
    $("#navlist li a").each(function(){
        var hreflink = $(this).attr("href");
        if (hreflink.toLowerCase() ==
            window.location.pathname.toLowerCase()) {
            $(this).addClass("navitem_selected");
        }
    });
}

function expand_list() {
    $("img.expandlist").click(function(event) {
        $(this).toggleClass("plus");
        $(this).toggleClass("minus");
        $(this).parent().nextUntil("dt").toggle();
    });

    $("dd").hide();
}

function expand_menu() {
    $(".collapse").click(function() {
        $(this).toggleClass("expanded");
        $(this).toggleClass("collapsed");
        $(this).nextUntil("h3").toggle();
    });
}

function date_picker() {
    $(".datepicker").datepicker({
        yearRange: "-40:+10",
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        beforeShow: function(input) {
             setTimeout(function() {
                var buttonPane = $(input).datepicker("widget")
                .find(".ui-datepicker-buttonpane");
                var btn = $('<button class="ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all" type="button">Clear</button>');
                btn.unbind("click").bind("click", function () {
                  $.datepicker._clearDate(input);
                });
                btn.appendTo(buttonPane);
            }, 0)
        },
    });
}

function shortcut_functions() {
    var d = new Date();
    $(".fall_semester").click(function() {
        $(this).parent().prev(".datepicker").datepicker("setDate", "09/01/" +
            d.getFullYear());
    });
    $(".winter_semester").click(function() {
        $(this).parent().prev(".datepicker").datepicker("setDate", "01/01/" +
            d.getFullYear());
    });
    $(".spring_semester").click(function() {
        $(this).parent().prev(".datepicker").datepicker("setDate", "05/01/" +
            d.getFullYear());
    });
}
