import { useParams, Navigate } from 'react-router-dom';
import { jobs } from '../data';
import { Briefcase, CheckCircle2, ChevronRight, Mail, MapPin } from 'lucide-react';
import { motion } from 'motion/react';

export default function JobDetails() {
  const { id } = useParams<{ id: string }>();
  const job = jobs.find((j) => j.id === id);

  if (!job) {
    return <Navigate to="/" replace />;
  }

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-12 max-w-3xl mx-auto"
    >
      {/* Header */}
      <header className="space-y-6 pb-8 border-b border-slate-200">
        <div className="flex flex-wrap items-center gap-y-3 gap-x-2 text-sm font-medium text-slate-500 uppercase tracking-wider">
          <div className="flex items-center gap-1.5 bg-slate-100 px-3 py-1.5 rounded-lg text-slate-600">
            <Briefcase size={16} className="shrink-0" />
            <span className="whitespace-nowrap">{job.type}</span>
          </div>
          <div className="flex items-center gap-1.5 bg-slate-100 px-3 py-1.5 rounded-lg text-slate-600">
            <MapPin size={16} className="shrink-0" />
            <span className="whitespace-nowrap">Hong Kong</span>
          </div>
        </div>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-slate-900 leading-tight">
          {job.title}
        </h1>
        <div className="flex flex-wrap gap-4 pt-4">
          <a 
            href={`mailto:${job.applyEmail}?subject=Application for ${job.title}`}
            className="inline-flex items-center justify-center gap-2 bg-slate-900 text-white px-6 py-3 rounded-xl font-medium hover:bg-slate-800 transition-colors focus:ring-4 focus:ring-slate-200"
          >
            <Mail size={18} />
            Apply for this job
          </a>
        </div>
      </header>

      <div className="space-y-16">
        {/* Responsibilities */}
        <section className="space-y-6">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900 flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center text-sm font-bold">1</div>
            Responsibilities
          </h2>
          <ul className="space-y-4">
            {job.responsibilities.map((item, index) => (
              <li key={index} className="flex items-start gap-4 text-slate-600 leading-relaxed">
                <CheckCircle2 size={20} className="text-blue-500 shrink-0 mt-1 opacity-70" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </section>

        {/* Requirements */}
        <section className="space-y-6">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900 flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-sm font-bold">2</div>
            Requirements
          </h2>
          <ul className="space-y-4">
            {job.requirements.map((item, index) => (
              <li key={index} className="flex items-start gap-4 text-slate-600 leading-relaxed">
                <CheckCircle2 size={20} className="text-emerald-500 shrink-0 mt-1 opacity-70" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </section>

        {/* What's On Offer */}
        <section className="bg-slate-50 rounded-3xl p-8 md:p-10 border border-slate-100">
          <h2 className="text-2xl font-semibold tracking-tight text-slate-900 mb-6">What's On Offer</h2>
          <ul className="space-y-4">
            {job.offer.map((item, index) => (
              <li key={index} className="flex items-center gap-3 text-slate-700 font-medium">
                <div className="w-2 h-2 rounded-full bg-violet-500 shrink-0" />
                {item}
              </li>
            ))}
          </ul>
          
          <div className="mt-10 pt-8 border-t border-slate-200">
            <p className="text-slate-600 mb-6 font-medium">
              Please send a full resume with current and expected salary to:
            </p>
            <a 
              href={`mailto:${job.applyEmail}?subject=Application for ${job.title}`}
              className="inline-flex items-center gap-3 text-lg font-semibold text-blue-600 hover:text-blue-700 transition-colors"
            >
              <Mail size={24} />
              {job.applyEmail}
            </a>
          </div>
        </section>
      </div>
    </motion.div>
  );
}
