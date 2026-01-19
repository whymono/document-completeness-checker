import UploadCard from "../components/UploadCard";
import Hero from "../components/Hero";
import Navbar from "../components/Navbar";
import ProblemCard from "../components/ProblemCard.jsx";

function LandingPage() {
  return (
    <>
        <Navbar />
        <Hero />
        <UploadCard />
        <ProblemCard problem={"Missing Documents"}/>
    </>
  );
}

export default LandingPage;
