import { BrowserRouter, Routes, Route } from "react-router-dom";
// import styled from "styled-components";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import NotFound from "./pages/NotFound";
import RegisterPage from "./pages/RegisterPage";
import SendingCodePage from "./pages/SendingCode";

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
          <Route path="/send_code" element={<SendingCodePage />}></Route>
          <Route element={<NotFound />}></Route>
        </Routes>
      </BrowserRouter>
    // </AppContainer>
  );
}

export default Router;