function CustomFileBrowser(field_name, url, type, win)
{
    // Use first line on info.science.uva.nl, second on development machine
    // var cmsURL = "/cgi-bin/api/admin/filebrowser/?pop=2&type=" + type;
    var cmsURL = "/admin/filebrowser/?pop=2&type=" + type;
    tinyMCE.activeEditor.windowManager.open(
    {
        file: cmsURL,
        width: 800,  // Your dimensions may differ - toy around with them!
        height: 500,
        resizable: "yes",
        scrollbars: "yes",
        inline: "no",  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: "no"
    },
    {
        window: win,
        input: field_name,
        editor_id: tinyMCE.selectedInstance.editorId
    });
    return false;
}

tinyMCE.init(
{
    mode: "exact",
    elements: "text,description",  // only the 'name=text' & 'name=description' textarea elements
    theme: "advanced",
    width: 600,
    height: 400,
    theme_advanced_blockformats: "p,h3,h4,blockquote",
    theme_advanced_buttons1: "undo,redo,|,bold,italic,underline,|,bullist,sub,sup,|,justifycenter,formatselect,|,link,unlink,anchor,image,|,code,cleanup,|,fullscreen,help",
    theme_advanced_buttons2: "",
    theme_advanced_buttons3: "",
    relative_urls : false,
    plugins : "safari,advimage,fullscreen",
    extended_valid_elements : "a[name|href|target|title|onclick],iframe[src|width|height|name|align|frameborder]",
    file_browser_callback : "CustomFileBrowser"
}
);
