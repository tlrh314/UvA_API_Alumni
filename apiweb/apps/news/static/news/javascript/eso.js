var sdfile = 'http://www.eso.org/public/archives/videos/medium_flash/eso1230a.flv';
var imagefile = 'http://www.eso.org/public/archives/videos/videoframe/eso1230a.jpg';
var flashsrc = 'http://www.eso.org/public/archives/djangoplicity/shadowbox3/libraries/mediaplayer5/player.swf';
var sharelink = 'http://www.eso.org/public/netherlands/videos/eso1230a/';
var sharecode = '';
var gaid = 'UA-1965004-1';
var ipadfile = 'http://www.eso.org/public/archives/videos/medium_podcast/eso1230a.m4v';
var mobilefile = 'http://www.eso.org/public/archives/videos/medium_podcast/eso1230a.m4v';
var hdfile = 'http://www.eso.org/public/archives/videos/hd_and_apple/eso1230a.m4v';


if(sdfile)
{
    var config = {  
	file: sdfile, 
	width: 580, 
	height: 326,
	autostart: false,
	players : [
    { type : "flash", src: flashsrc },
    { type : "html5" }
		   ],
	backcolor : "0x000000",
	frontcolor: "0xCCCCCC",
	lightcolor : "0x005ba0"
    };
    if( imagefile ) {
	config.image = imagefile;
    }
    if( jwplayer.utils.hasFlash() ) {
	config.plugins = {
	    sharing : { link : sharelink , code : sharecode },
	    gapro: { accountid: gaid }
	};
	if( hdfile ) {
	    config.plugins.hd = { file: hdfile }
	}
    } else {
	var isiPad = navigator.userAgent.match(/iPad/i) != null;
	
	if( isiPad ) {
	    config.file = ipadfile;
	} else {
	    config.file = mobilefile;
	}
    }
    jwplayer("filmpje").setup( config );
}
