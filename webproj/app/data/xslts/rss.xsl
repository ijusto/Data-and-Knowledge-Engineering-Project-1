<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <!-- Blog Post -->
        <xsl:for-each select="//item">
            <div class="d-flex flex-row" style="min-width: 0;
                                                word-wrap: break-word;
                                                background-color: #fff;
                                                background-clip: border-box;
                                                border: 1px solid rgba(0, 0, 0, 0.125);
                                                border-radius: 0.25rem;
                                                border-bottom-right-radius: 0.25rem;
                                                border-bottom-left-radius: 0.25rem;">
                <div class="p-2">
                    <xsl:attribute name="style">width: 50%; height: 50%</xsl:attribute>
                    <!--<img class="card-img-top" src="" alt="Card image cap"/>-->
                    <img>                        <xsl:attribute name="style">"width: 50%; height: 50%"</xsl:attribute>

                        <xsl:attribute name="src"><xsl:value-of select="enclosure/@url"/></xsl:attribute>
                        <xsl:attribute name="alt">Card image cap</xsl:attribute>
                        <xsl:attribute name="class">card-img-top</xsl:attribute>
                    </img>
                </div>
                <div class="p-2">
                    <!--<div class="card-body" style="align-items: baseline">-->
                    <h2><!--class="card-title"--><xsl:value-of select="title"/></h2>
                    <p><xsl:value-of select="description"/></p>
                    <!--</div>-->
                </div>
            </div>
            <div class="d-flex flex-row" style="min-width: 0;
                                                word-wrap: break-word;
                                                background-color: #fff;
                                                background-clip: border-box;
                                                border: 1px solid rgba(0, 0, 0, 0.125);
                                                border-radius: 0.25rem;
                                                border-bottom-right-radius: 0.25rem;
                                                border-bottom-left-radius: 0.25rem;
                                                margin-bottom: 1.5rem !important;">

                <div class="p-2">
                    <div class="card-footer text-muted">
                        <xsl:value-of select="pubDate"/>
                        <a href="https://www.cinemablend.com">CinemaBlend Latest Content</a>
                    </div>
                </div>
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>