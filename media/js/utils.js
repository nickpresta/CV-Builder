tinyMCE.init({
        // General options
        mode: "textareas",
        theme: "advanced",
        content_css: "/media/css/tinymce_style.css?" + new Date().getTime(),
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
        editor_deselector: "mceNoEditor",
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
        dateFormat: 'yy-mm-dd',
        yearRange: "-40:+10",
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        constrainInput: false,
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
        $(this).parent().prev(".datepicker").datepicker("setDate", d.getFullYear() + "-09-01");
    });
    $(".winter_semester").click(function() {
        $(this).parent().prev(".datepicker").datepicker("setDate", d.getFullYear() + "-01-01");
    });
    $(".spring_semester").click(function() {
        $(this).parent().prev(".datepicker").datepicker("setDate", d.getFullYear() + "-05-01");
    });
}

function removeYear() {
    $(this).parents("tr").remove();
    
    if ($("#distribution_table tr").length == 1)
        $("#distribution_table tr:first").hide();
            
    return false;
}

function multiItemTable_functions() {

    $(".additem").each(function(index) {
        var blankRow = $(this).next().find("tr:last");
        var totalForms = $(this).siblings("#id_form-TOTAL_FORMS");
        var prefix_regex = new RegExp("((id_form|form)-\\d+)");

        $(blankRow).datepicker("destroy");

        $(blankRow).find("input").each(function(index) {
            if (this.id)
                this.id = this.id.replace(prefix_regex, "");
            if (this.name)
                this.name = this.name.replace(prefix_regex, "");
        });

        $(totalForms).addClass("hidden");
        blankRow.hide();

        $(this).click(function() {
            var newRow = blankRow.clone(true, true);
            var formCount = parseInt($(totalForms).val()) - 1;
            var newPrefix = "form-" + formCount;

            $(newRow).find("input").each(function(index) {
                if (this.id)
                    this.id = "id_" + newPrefix + this.id;
                if (this.name)
                    this.name = newPrefix + this.name;
            });

            newRow.show();
            newRow.appendTo($(this).next());

            $(totalForms).val(formCount + 1);

            $(".datepicker").datepicker("destroy");
            date_picker();

            return false;
        });

    });

    $(".removeitem").click(function() {
        var parentTable = $(this).parents("table");
        var index_regex = new RegExp("(form-\\d+)");

        var rows;

        $(this).parents("tr").addClass("hidden");
        $(this).closest("td").siblings().find(".multiitem_delete").val(true);
        rows = $(parentTable).find(".multiitem_row").not(".hidden");

        for (var i = 0, formCount = rows.length; i < formCount; i++) {
            $(rows.get(i)).not(".hidden").find("input").each(function(index) {
                if (this.id)
                    this.id = this.id.replace(index_regex, "form-" + i);
                if (this.name)
                    this.name = this.name.replace(index_regex, "form-" + i);
            });
        }

        $(parentTable).siblings("#id_form-TOTAL_FORMS").val(rows.length - 1);

        return false;
    });
}

function executive_functions() {
    var blankRow = $("#distribution_blankrow").detach();

    blankRow.find('.datepicker').datepicker('destroy');

    $("#distribution_addyear").click(function() {
        var newRow = blankRow.clone(true, true);
        newRow.find(".distribution_removeyear").click(removeYear);
        newRow.find(".datepicker").datepicker();
        newRow.appendTo("#distribution_table");
        
        $("#distribution_table tr:first").show();

        date_picker();
        
        return false;
    });

    $(".distribution_removeyear").click(removeYear);
    
    if ($("#distribution_table tr").length == 1)
        $("#distribution_table tr:first").hide();
}

