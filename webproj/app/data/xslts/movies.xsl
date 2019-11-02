<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <!-- Blog Post -->
        <xsl:for-each select="/movies/movie">
            <div class="card mb-4">
                <img>
                    <xsl:attribute name="src">
                        <xsl:value-of select="poster"/>
                    </xsl:attribute>
                    <xsl:attribute name="alt">"Card image cap"</xsl:attribute>
                </img>
                <!--<img class="card-img-top" src="" alt="Card image cap"/>-->
                <div class="card-body">
                    <h2 class="card-title"><xsl:value-of select="title/name"/></h2>
                    <p class="card-text">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Reiciendis aliquid atque, nulla? Quos cum ex quis soluta, a laboriosam. Dicta expedita corporis animi vero voluptate voluptatibus possimus, veniam magni quis!</p>
                    <a href="#" class="btn btn-primary">Read More ...</a>
                </div>
                <div class="card-footer text-muted">
                    Posted on January 1, 2017 by
                    <a href="#">Start Bootstrap</a>
                </div>
            </div>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>