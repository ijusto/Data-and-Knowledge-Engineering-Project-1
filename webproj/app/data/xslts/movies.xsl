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
                    <h2><!--class="card-title"--><xsl:value-of select="title/name"/></h2>
                    <p><!-- class="card-text"-->Lorem ipsum dolor sit amet, consectetur adipisicing elit. Reiciendis aliquid atque, nulla? Quos cum ex quis soluta, a laboriosam. Dicta expedita corporis animi vero voluptate voluptatibus possimus, veniam magni quis!</p>
                    <a href="#" class="btn btn-primary">Read More ...</a>
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