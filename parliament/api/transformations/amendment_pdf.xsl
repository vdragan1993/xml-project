<?xml version="1.0"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:a = "http://ftn.uns.ac.rs/xml"
    xmlns:b="https://ftn.uns.ac.rs/xml"
    version="2.0">
    
    <xsl:template match="/">
        <html>
            <head>
                <meta charset="UTF-8" />
                <title>Amandman</title>
                <style type="text/css">
                    body { font-family: "Arial", sans-serif; 
                           text-align: center;  
                           margin-top: 3%;
                           margin-bottom: 3%;}
                    img { height: 100; width: 100; }
                    h1 {text-transform: uppercase;}
                    p#clan { text-align: justify; margin-left:20%; margin-right:20%; display:block;
                            border: 1px solid; padding: 1%;}
                    p#obrazlozenje {text-align:justify; margin-left:20%; margin-right:20%; display:block;}
                    p#potpis{text-align: left; margin-left:20%;}
                </style>
            </head>
            
            <body>   
                <h1>Amandman</h1>
                <br />
                <h3>za Akt &#160;<a href="{/*/@uri}" target="_blank"><xsl:value-of select="/*/@uri"/></a></h3>
                <br />
                <br />
                <h2><xsl:value-of select="/*/@operacija"/> za Član broj <xsl:value-of select="//a:clan/@rbr"/>. <i><xsl:value-of select="//a:clan[1]/@naslov"/></i></h2>
                <br />
                <br />
                <br />
                <h4>Predlog Amandmana</h4>
                <br />
                <p id="clan">
                    <xsl:value-of select="//a:clan"/>
                </p>
                <br />
                <br />
                <h4>Obrazloženje</h4>
                <br />
                <p id="obrazlozenje">
                    <xsl:value-of select="//b:obrazlozenje"/>
                </p>
                <br />
                <br />
                <p id="potpis">U Novom Sadu, <xsl:value-of select="/*/@datum"/>
                <br />
                <xsl:value-of select="/*/@predlagac"/></p>
            </body>
        </html>
    </xsl:template>
    
</xsl:stylesheet>