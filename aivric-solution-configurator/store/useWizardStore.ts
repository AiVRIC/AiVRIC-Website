import create from 'zustand';
import { persist } from 'zustand/middleware';

type WizardState = {
  stepIndex: number;
  data: any;
  persona?: string;
  setData: (patch: any) => void;
  setStep: (i: number) => void;
  setPersona: (p?: string) => void;
  reset: () => void;
};

export const useWizardStore = create<WizardState>()(
  persist(
    (set, get) => ({
      stepIndex: 0,
      data: {},
      persona: undefined,
        setData: (patch) => set({ data: { ...get().data, ...patch } }),
        setStep: (i) => set({ stepIndex: i }),
        setPersona: (p) => set({ persona: p }),
        reset: () => set({ stepIndex: 0, data: {}, persona: undefined })
    }),
    { name: 'aivric-wizard' }
  )
);
