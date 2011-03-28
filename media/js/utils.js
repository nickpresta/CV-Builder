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

function multiItemTable_functions() {

    $(".multiitem_table").each(function(index) {
        var blankRow = $(this).find("tr:last");
        var totalForms = $(this).siblings("#id_form-TOTAL_FORMS");
        var prefix_regex = new RegExp("((id_form|form)-\\d+)");

        // take the last row of the table and make it the "blank row", which will
        // be cloned to make new rows
        $(blankRow).find("input").each(function(index) {
            if (this.id)
                this.id = this.id.replace(prefix_regex, "");
            if (this.name)
                this.name = this.name.replace(prefix_regex, "");
        });

        blankRow.hide();        

        // decrement the form managers total form count
        $(totalForms).val(parseInt($(totalForms).val()) - 1);

        // add row inserts a duplicate of the last row of the table, which is
        // hidden
        $(this).find(".additem").click(function() {
            var newRow = blankRow.clone(true);
            var formCount = parseInt($(totalForms).val());
            var newPrefix = "form-" + formCount;

            // change the name and id of the new row's inputs
            $(newRow).find("input").each(function(index) {
                if (this.id)
                    this.id = "id_" + newPrefix + this.id;
                if (this.name)
                    this.name = newPrefix + this.name;
            });

            newRow.appendTo($(this).parents(".multiitem_table")).show();

            // increment the form manager form count
            $(totalForms).val(formCount + 1);

            // when inserting a new date picker element, all previous
            // datepicker's must be destroyed, then recreated
            $(".datepicker").datepicker("destroy");
            date_picker();

            return false;
        });

        // replace Django's delete checkboxes with hidden inputs
        $(this).find("input:checkbox[id $= '-DELETE']").each(function () {
            $(this).before("<input type='hidden' id='id_" + this.id + "' name='" + this.name + "' />");
            $(this).remove();
        });

    });

    // delete row marks the hidden delete input as on and hides the row
    $(".removeitem").click(function() {
        $(this).parents("tr").find('input:hidden[id $= "-DELETE"]').val('on');
        $(this).parents("tr").hide();
        $(this).parents("tr").addClass("hidden");

        // when inserting a new date picker element, all previous
        // datepicker's must be destroyed, then recreated
        $(".datepicker").datepicker("destroy");
        date_picker();

        return false;
    });    
}
