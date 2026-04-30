import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import CentreDeCongres from "./pages/CentreDeCongres";
import Element from "./pages/Element";
import Evenement from "./pages/Evenement";
import Option from "./pages/Option";
import Materiel from "./pages/Materiel";
import Prestation from "./pages/Prestation";
import Gestionaire from "./pages/Gestionaire";
import Reservation from "./pages/Reservation";
import Indisponiblite from "./pages/Indisponiblite";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/centre_de_congres" element={<CentreDeCongres />} />
            <Route path="/element--------------------------------------------------------" element={<Element />} />
            <Route path="/evenement" element={<Evenement />} />
            <Route path="/option" element={<Option />} />
            <Route path="/materiel" element={<Materiel />} />
            <Route path="/prestation" element={<Prestation />} />
            <Route path="/gestionaire" element={<Gestionaire />} />
            <Route path="/reservation" element={<Reservation />} />
            <Route path="/indisponiblite" element={<Indisponiblite />} />
            <Route path="/" element={<Navigate to="/centre_de_congres" replace />} />
            <Route path="*" element={<Navigate to="/centre_de_congres" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
