<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <!-- Blog Post -->
        <xsl:for-each select="/movies/movie">
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
                    <!--<img class="card-img-top" src="" alt="Card image cap"/>-->
                    <img>
                        <xsl:attribute name="src">
                            <xsl:value-of select="poster"/>
                        </xsl:attribute>
                        <xsl:attribute name="alt">"Card image cap"</xsl:attribute>
                        <xsl:attribute name="class">"card-img-top"</xsl:attribute>
                    </img>
                </div>
                <div class="p-2">
                    <!--<div class="card-body" style="align-items: baseline">-->
                    <h2>
                        <a>
                            <xsl:attribute name="href">movie/<xsl:value-of select="title/name"/>/</xsl:attribute>
                            <xsl:value-of select="title/name"/>
                        </a>
                    </h2>
                    <p>
                        <xsl:for-each select="genres/genre">
                            [<xsl:value-of select="."/>]
                        </xsl:for-each>
                        (<xsl:value-of select="title/year"/>)
                    </p>
                    <p><strong><i>Director:</i></strong> <xsl:value-of select="director//name"/></p>
                    <p>
                        <strong><i>Cast: </i></strong>
                            <br/>
                            <xsl:for-each select="cast/main_actors//name">
                            - <xsl:value-of select="."/>
                            <br/>
                        </xsl:for-each>
                    </p>
                    <p><strong><xsl:value-of select="imbd_info/score"/></strong>/10</p>
                    <!--</div>-->
                </div>
                <!--
                <div class="card-footer text-muted">
                    Posted on January 1, 2017 by
                    <a href="#">Start Bootstrap</a>
                </div>
                -->
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>