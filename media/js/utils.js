tinyMCE.init({
        // General options
        mode: "textareas",
        theme: "advanced",
        content_css: "/media/css/tinymce_style.css?" + new Date().getTime(),
        plugins:
        "pagebreak,style,layer,table,advhr,advimage,advlink,iespell,inlinepopups,insertdatetime,preview,searchreplace,contextmenu,paste,directionality,fullscreen,noneditable,xhtmlxtras,template",
        theme_advanced_buttons1:
        "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull",//,formatselect,fontselect,fontsizeselect",
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
        editor_deselector: "mceNoEditor"
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

function expand_collapse_all() {
    $("#expand_all").click(function() {
        $("img.expandlist").removeClass("plus");
        $("img.expandlist").addClass("minus");
        $("img.expandlist").parent().nextAll("dd").show();
        sessionStorage.setItem('menu', 'expanded');
    });
    $("#collapse_all").click(function() {
        $("img.expandlist").removeClass("minus");
        $("img.expandlist").addClass("plus");
        $("img.expandlist").parent().nextAll("dd").hide();
        sessionStorage.setItem('menu', 'collapsed');
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
        }
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
    var removeNum_regex = new RegExp("(-\\d+-)");
    var addNum_regex = new RegExp("(__prefix__)");

    $(".multiitem_table").each(function(index) {
        var blankRow = $(this).find("tr:last");
        var totalFormsElem = $(this).siblings("input:hidden[id $= '-TOTAL_FORMS']");

        blankRow.hide();
        
        if ($(this).find(".multiitem_row:visible").length == 0)
            $(this).find(".multiitem_header").hide();


        // add new row, insert duplicate of last row (blankRow) in table
        $(this).find(".additem").click(function() {
            var newRow = blankRow.clone(true);
            var formCount = parseInt($(totalFormsElem).val());

            $(this).closest(".multiitem_table").find(".multiitem_header").show();

            // change the numbering of the new row's inputs
            $(newRow).find("[name *= \"__prefix__\"]").each(function(index) {
                if (this.id)
                    this.id = this.id.replace(addNum_regex, formCount);
                if (this.name)
                    this.name = this.name.replace(addNum_regex, formCount);
            });

            newRow.appendTo($(this).parents(".multiitem_table")).show();

            // increment the form manager form count
            $(totalFormsElem).val(formCount + 1);

            // when inserting a new date picker element, all previous
            // datepicker's must be destroyed, then recreated
            $(".datepicker").datepicker("destroy");
            date_picker();

            return false;
        });

        // replace Django's delete checkboxes with hidden inputs
        $(this).find("input:checkbox[id $= '-DELETE']").each(function () {
            $(this).before("<input type='hidden' id='" + this.id + "' name='" + this.name + "' />");
            $(this).remove();
        });

    });

    // delete row
    $(".removeitem").click(function() {
        // mark hidden delete input as on
        $(this).parents("tr").find('input:hidden[id $= "-DELETE"]').val('on');

        $(this).parents("tr").hide();
        $(this).parents("tr").addClass("hidden");

        // when inserting a new date picker element, all previous
        // datepicker's must be destroyed, then recreated
        $(".datepicker").datepicker("destroy");
        date_picker();

        
        if ($(this).closest(".multiitem_table").find(".multiitem_row:visible").length == 0)
            $(this).closest(".multiitem_table").find(".multiitem_header").hide();

        return false;
    });

    // show all rows with errors
    $(".multiitem_table tr:has(td.error)").show();
}

function settings() {
    if (sessionStorage.getItem("menu")) {
        if (sessionStorage.getItem("menu") == "expanded") {
            $("#expand_all").trigger("click");
        }
    }
}

function enable_autocomplete() {
    $("#id_facultydepartments-departments").autocomplete({ source : "/autocomplete/?table=departments" });
}
