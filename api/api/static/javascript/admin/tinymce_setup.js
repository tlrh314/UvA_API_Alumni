tinyMCE.init({

    // see http://www.tinymce.com/wiki.php
    //
    // docs/fieldswidgets.rst - Using the FileBrowseField with TinyMCE
    // class Media:
    //     js = ['/path/to/your/tinymce/tinymce.min.js',
    //           '/path/to/your/tinymce_setup.js']

    width: 900,  // Your dimensions may differ - toy around with them!
    height: 400,

    theme: "modern",
    skin : 'lightgray',

    selector:'textarea[name=text], textarea[name=description]',

    plugins: [
        "link image anchor image code fullscreen",
    ],

    relative_urls: false,

    image_advtab: true,

    extended_valid_elements: "a[name|href|target|title|onclick],iframe[src|width|height|name|align|frameborder]",

// if you comment out the style_formats, you will get all the options under styleselect
    style_formats: [
          {title: 'Paragraph',  format: 'p'},
          {title: 'Header 3',   format: 'h3'},
          {title: 'Header 4',   format: 'h4'},
          {title: 'Blockquote', format: 'blockquote'}
    ],

    menubar: false,
    toolbar: "undo redo | bold italic underline | bullist numlist subscript superscript | aligncenter styleselect removeformat | link unlink anchor image | code | fullscreen help",

//  setup : function(ed) {
//    ed.on('init', function(evt) {
//        ed.getBody().setAttribute('spellcheck', true);
//    });
//  },

    file_browser_callback: function(input_id, input_value, type, win){
        var cmsURL = '/admin/filebrowser/browse/?pop=4';
        cmsURL = cmsURL + '&type=' + type;

        tinymce.activeEditor.windowManager.open({
            file: cmsURL,
            width: 900,  // Your dimensions may differ - toy around with them!
            height: 500,
            resizable: 'yes',
            scrollbars: 'yes',
            inline: 'no',  // This parameter only has an effect if you use the inlinepopups plugin!
            close_previous: 'no'
        }, {
            window: win,
            input: input_id,
        });
        return false;
    },
});
