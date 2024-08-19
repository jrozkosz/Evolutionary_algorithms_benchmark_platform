import { BrowserRouter, Routes, Route } from "react-router-dom";
// import styled from "styled-components";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import NotFound from "./pages/NotFound";
import RegisterPage from "./pages/RegisterPage";
import SendingCodePage from "./pages/SendingCodePage";
import ConfirmEmailPage from "./pages/ConfirmEmail";
import AlgorithmRunningProgressPage from "./not_used/AlgorithmRunningProgressPage";
import AlgorithmsRankingsPage from "./pages/AlgorithmsRankingsPage";
import InformationPage from "./pages/InformationPage";
import AdminPanelPage from "./pages/AdminPanelPage";

// const AppContainer = styled.div`
//   width: 100%;
//   height: 100%;
// `;

function Router() {
  return (
    // <AppContainer>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />}></Route>
          <Route path="/login" element={<LoginPage />}></Route>
          <Route path="/register" element={<RegisterPage />}></Route>
          <Route path="/confirm/:token" element={<ConfirmEmailPage />}></Route>
          <Route path="/upload" element={<SendingCodePage />}></Route>
          <Route path="/algorithms_rankings" element={<AlgorithmsRankingsPage />}></Route>
          <Route path="/information" element={<InformationPage />}></Route>
          <Route path="/admin_panel" element={<AdminPanelPage />}></Route>
          <Route element={<NotFound />}></Route>
        </Routes>
      </BrowserRouter>
    // </AppContainer>
  );
}

export default Router;