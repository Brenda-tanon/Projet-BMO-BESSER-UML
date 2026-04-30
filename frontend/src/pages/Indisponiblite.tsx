import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Indisponiblite: React.FC = () => {
  return (
    <div id="page-indisponiblite-8">
    <div id="i6prow" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="io15k7" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i7iv95" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i4clbw" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ipjt2j" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/centre_de_congres">{"Centre_de_congres"}</a>
          <a id="izefq6" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/element                                                        ">{"Element"}</a>
          <a id="ilnq6o" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/evenement">{"Evenement"}</a>
          <a id="ii7ju6" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/option">{"option"}</a>
          <a id="izkaqg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/materiel">{"materiel"}</a>
          <a id="i6vc8b" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/prestation">{"prestation"}</a>
          <a id="i2ase2" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/gestionaire">{"gestionaire"}</a>
          <a id="ihzdj2" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/reservation">{"Reservation"}</a>
          <a id="iws425" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/indisponiblite">{"Indisponiblite"}</a>
        </div>
        <p id="iy3agi" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i7683k" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ishmak" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Indisponiblite"}</h1>
        <p id="ic9h7s" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Indisponiblite data"}</p>
        <TableBlock id="table-indisponiblite-8" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Indisponiblite List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Date Debut", "column_type": "field", "field": "date_debut", "type": "date", "required": true}, {"label": "Date Fin", "column_type": "field", "field": "date_fin", "type": "date", "required": true}, {"label": "Motif", "column_type": "field", "field": "motif", "type": "str", "required": true}, {"label": "Sale Evenement", "column_type": "field", "field": "sale_evenement", "type": "any", "required": true}], "formColumns": [{"column_type": "field", "field": "date_debut", "label": "date_debut", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "date_fin", "label": "date_fin", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "motif", "label": "motif", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "sale_evenement", "label": "sale_evenement", "type": "any", "required": true, "defaultValue": null}]}} dataBinding={{"entity": "Indisponiblite", "endpoint": "/indisponiblite/"}} />
      </main>
    </div>    </div>
  );
};

export default Indisponiblite;
