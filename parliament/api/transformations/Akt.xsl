<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:b="http://ftn.uns.ac.rs/xml"
    version="2.0">
    
    <xsl:template match="/">
        <html>
            <head>
                <meta charset="UTF-8"/>
            </head>
            <body style="font-family: Arial">
                <div style="text-align: center; margin-bottom: 15px">
                    <img src="http://www.nirvot.org.rs/nsgrb2.gif" height="100" width="100"/>
                </div>
                
                <xsl:apply-templates select="//b:preambula"/>
                <h2 style="text-align: center">
                    <xsl:value-of select="b:akt/@naslov"/>
                </h2>
                <xsl:apply-templates select="b:akt/*[not(self::b:preambula)]"/>
            </body>
        </html>
    </xsl:template>
    
    <!-- Preambula -->
    <xsl:template match="b:preambula">
        <p>
            <xsl:value-of select="."/>
        </p>
    </xsl:template>
    
    <!-- Deo -->
    <xsl:template match="b:deo">
        <h3 style="text-align: center">
            <xsl:value-of select="@naslov"/>
        </h3>
        <xsl:choose>
            <xsl:when test="count(b:glava) &gt; 0">
                <ol>
                    <xsl:apply-templates select="b:glava"/>
                </ol>
            </xsl:when>
            <xsl:otherwise>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- Glava -->
    <xsl:template match="b:glava">
        <h3 style="text-align: center">
            <xsl:value-of select="@naslov"/>
        </h3>
        <xsl:choose>
            <xsl:when test="count(b:clan) &gt; 0">
                <xsl:apply-templates select="b:clan"/>
            </xsl:when>
            <xsl:when test="count(b:odeljak) &gt; 0">
                <xsl:apply-templates select="b:odeljak"/>
            </xsl:when>
            <xsl:otherwise/>
        </xsl:choose>
    </xsl:template>
    
    <!-- Clan -->
    <xsl:template match="b:clan">
        <div>
            <xsl:choose>
                <xsl:when test="count(b:clan/@naslov) &gt; 0">
                    <xsl:value-of select="@naslov"/>
                </xsl:when>
                <xsl:otherwise/>
            </xsl:choose>
            
            <!-- Add modify link 
            <xsl:choose>
                <xsl:when test="@modify">
                    <a>
                        <xsl:attribute name="href">
                            <xsl:value-of select="@modify"/>
                        </xsl:attribute>
                        <div style="text-align: center">Modify</div>
                    </a>
                </xsl:when>
            </xsl:choose>-->
            
            <h3 style="text-align: center">
                Član <xsl:value-of select="@rbr"/>
            </h3>
            <xsl:choose>
                <xsl:when test="count(b:stav) &gt; 0">
                    <xsl:apply-templates select="b:stav"/>
                </xsl:when>
                <xsl:otherwise>
                </xsl:otherwise>
            </xsl:choose>
        </div>
    </xsl:template>
    
    <!-- Odeljak -->
    <xsl:template match="odeljak">
        <h3 style="text-align: center">
            <xsl:value-of select="@naslov"/>
        </h3>
        <xsl:choose>
            <xsl:when test="count(b:pododeljak) &gt; 0">
                <xsl:apply-templates select="b:pododeljak"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="b:clan"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- Stav -->
    <xsl:template match="b:stav">
        <p>
            <xsl:value-of select="b:tekst"/>
        </p>
        <xsl:choose>
            <xsl:when test="count(b:tacka) &gt; 0">
                <ol>
                    <xsl:apply-templates select="b:tacka"/>
                </ol>
            </xsl:when>
            <xsl:otherwise>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- Pododeljak -->
    <xsl:template match="b:pododeljak">
        <h3 style="text-align: center">
            <xsl:value-of select="@naslov"/>
        </h3>
        <xsl:apply-templates select="b:article"/>
    </xsl:template>
    
    <!-- Tacka -->
    <xsl:template match="b:tacka">
        <xsl:choose>
            <xsl:when test="count(b:podtacka) &gt; 0">
                <xsl:apply-templates select="b:podtacka"/>
            </xsl:when>
            <xsl:otherwise>
                <li>
                    <xsl:value-of select="."/>
                </li>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- Podtacka -->
    <xsl:template match="b:podtacka">
        <xsl:choose>
            <xsl:when test="count(b:alineja) &gt; 0">
                <ol>
                    <xsl:apply-templates select="b:alineja"/>
                </ol>
            </xsl:when>
            <xsl:otherwise>
                <ol>
                    <xsl:value-of select="."/>
                </ol>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <!-- Alineja -->
    <xsl:template match="b:alineja">
        <li>
            <xsl:value-of select="."/>
        </li>
    </xsl:template>
    
</xsl:stylesheet>