import React from 'react';
import { motion } from 'framer-motion';

const Hero = () => {
  return (
    <div className="hero-container">
      <motion.h1
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
      >
        Document Completeness Checker
      </motion.h1>
      <motion.h2
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.3 }}
      >
        Upload your PDF and let our AI instantly identify any missing information.
      </motion.h2>
    </div>
  );
};

export default Hero;
