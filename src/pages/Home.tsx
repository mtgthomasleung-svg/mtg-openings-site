import { Building2, CheckCircle2, Globe2, Users } from 'lucide-react';
import { companyInfo } from '../data';
import { motion } from 'motion/react';

export default function Home() {
  const overviewParagraphs = companyInfo.overview
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-16"
    >
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <div className="space-y-4">
          <h1 className="text-2xl md:text-3xl font-semibold tracking-tight text-slate-900">
            Careers at Mobigator
          </h1>
          <p className="text-lg md:text-xl text-slate-500 max-w-2xl mx-auto leading-relaxed">
            Join an amazingly talented team to design and develop advanced business applications.
          </p>
        </div>
        <div className="inline-flex items-center justify-center p-4 bg-white rounded-2xl shadow-sm border border-slate-100 mb-6">
          <img src={companyInfo.logo} alt={companyInfo.name} className="h-16 md:h-20 object-contain" referrerPolicy="no-referrer" />
        </div>
        <div className="space-y-1">
          <p className="text-lg md:text-xl font-semibold tracking-wide text-slate-700">
            Healthcare IT Solutions
          </p>
          <p className="text-base md:text-lg text-slate-500">
            Where Programmers Can Save Lives
          </p>
        </div>
      </section>

      {/* Overview */}
      <section className="bg-white rounded-3xl p-8 md:p-12 shadow-sm border border-slate-100 relative overflow-hidden">
        <div className="absolute top-0 right-0 -mt-16 -mr-16 text-slate-50 opacity-50 pointer-events-none">
          <Globe2 size={240} />
        </div>
        <div className="relative z-10 space-y-6">
          <div className="flex items-center gap-3 text-blue-600 mb-4">
            <Building2 size={24} />
            <h2 className="text-2xl font-semibold tracking-tight text-slate-900">Overview</h2>
          </div>
          <div className="space-y-5 text-slate-600 leading-relaxed">
            {overviewParagraphs.map((paragraph) => (
              <p key={paragraph}>{paragraph}</p>
            ))}
          </div>
        </div>
      </section>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Our Offer */}
        <section className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
          <div className="flex items-center gap-3 text-emerald-600 mb-6">
            <Users size={24} />
            <h2 className="text-2xl font-semibold tracking-tight text-slate-900">Our Offer</h2>
          </div>
          <p className="text-slate-600 leading-relaxed">
            {companyInfo.offer}
          </p>
        </section>

        {/* Benefits */}
        <section className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
          <div className="flex items-center gap-3 text-violet-600 mb-6">
            <CheckCircle2 size={24} />
            <h2 className="text-2xl font-semibold tracking-tight text-slate-900">Benefits</h2>
          </div>
          <p className="text-slate-600 leading-relaxed">
            {companyInfo.benefits}
          </p>
        </section>
      </div>
    </motion.div>
  );
}
